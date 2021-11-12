import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import panel as pn

def marginal_probability(prior, sens, spec):
    return sens*prior + (1-spec)*(1-prior) # P(B)

def posterior_probability(prior, sens, spec):
    return (sens*prior) / marginal_probability(prior, sens, spec)

def sens_from_grade(fn):
    return (100-grade[fn])/100

def spec_from_grade(fp):
    return (100-grade[fp])/100

grade = {'n/a':50, 'many':44, 'some':22, 'few':11, 'rare':6}

def convert_from_grade(howmany):
    return (100-grade[howmany])/100

def branch_prob(prior, p_pos, p_neg):
    return (prior - p_neg)/(p_pos - p_neg)

def plot_posterior(sens, spec):
    optl = dict(lw=4, color='red', ls='-')
    prior = np.linspace(0.1, 1.0)  # P(H)
    f, ax = plt.subplots(constrained_layout=True)
    ax.plot(prior, posterior_probability(prior, sens, spec), **optl)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
    ax.set_xlabel('Prior Probability P(H)')
    ax.set_ylabel('Posterior Probability P(H|A)')
    ax.set_title('Sensitivity: {}, Specificity: {}'.format(sens, spec))

def plot_posterior_grade(sens_grade, spec_grade):
    sens = convert_from_grade(sens_grade)
    spec = convert_from_grade(spec_grade)
    prior = np.linspace(0.1, 1.0)  # P(H)
    optl = dict(lw=4, color='red', ls='-')
    f, ax = plt.subplots(figsize=(5, 5), constrained_layout=True)
    ax.plot(prior, posterior_probability(prior, sens, spec), **optl)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
    ax.set_xlabel('Prior Probability P(H)')
    ax.set_ylabel('Posterior Probability P(H|A)')
    ax.set_title('Sensitivity: {}={}, Specificity: {}={}'.format(
        sens_grade, sens, spec_grade, spec))

def pn_plot_posterior(sens_grade='many', spec_grade='many'):
    sens = convert_from_grade(sens_grade)
    spec = convert_from_grade(spec_grade)
    prior = np.linspace(0.1, 1.0)  # P(H)
    optl = dict(lw=4, color='red', ls='-')
    fig = Figure(figsize=(8, 8))
    ax = fig.subplots()
    ax.plot(prior, posterior_probability(prior, sens, spec), **optl)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
    ax.set_xlabel('Prior Probability P(H)')
    ax.set_ylabel('Posterior Probability P(H|A)')
    ax.set_title('Sensitivity: {}={}, Specificity: {}={}'.format(
        sens_grade, sens, spec_grade, spec))
    return pn.pane.Matplotlib(fig)


def pn_simulation_posterior(pos=(0.6,0.8), sens=0.5, spec=0.5, noise_hi=0.05, ns='medium'):
    rng = np.random.default_rng()
    howmany = ['low', 'medium', 'high']
    howmany_number =  [20, 200, 2000]
    samples = dict(zip(howmany,howmany_number))
    noise = rng.uniform(low=0.00, high=noise_hi, size=samples[ns])
    prior = rng.normal(loc=np.mean(pos), scale=np.std(pos), size=samples[ns])
    opt = dict(marker='o', markersize=10, mec='none', ls='none', alpha=20/samples[ns], color='k')
    optl = dict(fontsize=20)
    fig = Figure(figsize=(10, 10))
    ax = fig.subplots()
    ax.plot(prior, posterior_probability(prior, sens+noise, spec+noise), **opt)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid()
    ax.set_xlabel('Prior Probability P(H)', **optl)
    ax.set_ylabel('Posterior Probability P(H|A)', **optl)
    titletxt = 'Prior POS mean={:.2f}\nSensitivity={:.2f}, Specificity={:.2f}'
    ax.set_title(titletxt.format(np.mean(pos), sens, spec), **optl)
    ax.tick_params(axis='both', which='major', labelsize=14)
    return pn.pane.Matplotlib(fig)

def pn_simulation_posterior_v2(pos=(0.6,0.8), sens=0.5, spec=0.5, noise_hi=0.05, ns='medium'):
    rng = np.random.default_rng()
    howmany = ['low', 'medium', 'high']
    howmany_number =  [20, 200, 2000]
    samples = dict(zip(howmany,howmany_number))
    noise = rng.uniform(low=0.00, high=noise_hi, size=samples[ns])
    prior = rng.normal(loc=np.mean(pos), scale=np.std(pos), size=samples[ns])
    opt = dict(marker='o', markersize=10, mec='none', ls='none', alpha=20/samples[ns], color='k')
    optl = dict(fontsize=20)
    fig = Figure(figsize=(8, 10), constrained_layout=True)
    ax1 = fig.add_subplot(211)

    # ax = fig.subplots()
    ax1.plot(prior, posterior_probability(prior, sens+noise, spec+noise), **opt)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.grid()
    ax1.set_xlabel('Prior Probability P(H)', **optl)
    ax1.set_ylabel('Posterior Probability P(H|A)', **optl)
    titletxt = 'Prior POS mean={:.2f}\nSensitivity={:.2f}, Specificity={:.2f}'
    ax1.set_title(titletxt.format(np.mean(pos), sens, spec), **optl)
    ax1.tick_params(axis='both', which='major', labelsize=14)

    opth = dict(color='.5', lw=4, range=(0, 1), histtype='step', bins=20)
    # opth = dict(color='k', density=True)
    # opth = dict(color='k', bins=30, range=(0, 1), )
    #opth = dict(color='0.5', bins=50)
    ax2 = fig.add_subplot(325)
    ax2.hist(prior, **opth)
    ax2.set_xlabel('Prior Probability P(H)', fontsize=14)

    ax3 = fig.add_subplot(326)
    ax3.hist(posterior_probability(prior, sens+noise, spec+noise), **opth)
    ax3.set_xlabel('Posterior Probability P(H|A)', fontsize=14)

    return pn.pane.Matplotlib(fig)