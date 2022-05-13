import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import panel as pn

def marginal_probability(prior, sens, spec):
    return sens*prior + (1-spec)*(1-prior) # P(B)

def posterior_probability(prior, sens, spec):
    return (sens*prior) / marginal_probability(prior, sens, spec)

def branch_prob(prior, p_pos, p_neg):
    return (prior - p_neg)/(p_pos - p_neg)

def plot_posterior(sens, spec):
    optl = dict(lw=4, color='red', ls='-')
    prior = np.linspace(0.1, 1.0)
    f, ax = plt.subplots(constrained_layout=True)
    ax.plot(prior, posterior_probability(prior, sens, spec), **optl)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
    ax.set_xlabel('Prior Probability P(H)')
    ax.set_ylabel('Posterior Probability P(H|A)')
    ax.set_title('Sensitivity: {}, Specificity: {}'.format(sens, spec))

def pn_simulation_posterior_v2(pos=(0.6,0.8), sens=0.5, spec=0.5, noise_hi=0.05, ns='many', large_interface=False):
    if large_interface:
        optl = dict(fontsize=14)
        labsz = 12
        figsz = (10, 12)
    else:
        optl = dict(fontsize=10)
        labsz = 8
        figsz = (4, 5)
            
    rng = np.random.default_rng()
    howmany = ['few', 'many', 'overkill']
    howmany_number =  [20, 200, 2000]
    samples = dict(zip(howmany,howmany_number))
    noise = rng.uniform(low=0.00, high=noise_hi, size=samples[ns])
    prior = rng.normal(loc=np.mean(pos), scale=np.std(pos), size=samples[ns])
    
    # set options
    opt = dict(marker='o', markersize=10, mec='none', ls='none', alpha=20/samples[ns], color='k')
    opth = dict(color='.5', lw=4, range=(0, 1), histtype='step', bins=20)
   
    # make figure
    fig = Figure(figsize=figsz, constrained_layout=True)
    ax1 = fig.add_subplot(211)
    ax1.plot(prior, posterior_probability(prior, sens+noise, spec+noise), **opt)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.grid()
    ax1.set_xlabel('Prior Probability P(H)', **optl)
    ax1.set_ylabel('Posterior Probability P(H|A)', **optl)
    titletxt = 'P(H) mean={:.2f}\nSensitivity={:.2f}, Specificity={:.2f}'
    ax1.set_title(titletxt.format(np.mean(pos), sens, spec), **optl)
    ax1.tick_params(axis='both', which='major', labelsize=labsz)
    ax2 = fig.add_subplot(325)
    ax2.hist(prior, **opth)
    ax2.set_xlabel('Prior Probability P(H)', **optl)
    ax3 = fig.add_subplot(326)
    ax3.hist(posterior_probability(prior, sens+noise, spec+noise), **opth)
    ax3.set_xlabel('Posterior Probability P(H|A)', **optl)
    return pn.pane.Matplotlib(fig)