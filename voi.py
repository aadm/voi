from voi_funcs import *

#--- plot of prior vs post probability
# H=event, A=test
# posterior probability P(H|A) = P(A|H) * P(H) / P(A)
# posterior probability P(H|A) = sens*prior / (sens*prior + (1-spec)*(1-prior))

sens = np.linspace (0.1, 1)  # P(A|H)
spec = np.linspace (0.1, 1)  # P(~A|~H)

prior = np.linspace(0.1, 1.0, 10)  # P(H)


#--- plot of prior vs post probability
plot_posterior_grade('many', 'many')

plot_posterior_grade('few', 'few')

#--- plot prior vs post POS with different sens/spec
prior = np.linspace(0.1, 1.0)  # P(H)
acc = np.linspace(0.5, 0.9, 5)

k = 0.75
f, ax = plt.subplots(ncols=2, figsize=(10, 5), constrained_layout=True, sharey=True)
for i in acc:
    ax[0].plot(prior, posterior_probability(prior, i, k), label='Sens={}'.format(i))
    ax[1].plot(prior, posterior_probability(prior, k, i), label='Spec={}'.format(i))
for aa in ax:
    aa.set_xlim(0, 1.1)
    aa.set_ylim(0, 1.1)
    aa.grid()
    aa.set_xlabel('Prior Probability P(H)')
    aa.set_ylabel('Posterior Probability P(H|A)')
    aa.legend()
ax[0].set_title('Fixed Specificity: {}'.format(k))
ax[1].set_title('Fixed Sensitivity: {}'.format(k))




#--- 3d plot of sens/spec/post.prob
ss = np.linspace(0.1,1)
X0, Y0 = np.meshgrid(ss, ss)

priors = [0.3, 0.8]

f, ax = plt.subplots(ncols=2, figsize=(12,5),
                     subplot_kw={"projection": "3d"},
                     constrained_layout=True)
for i, val in enumerate(priors):
    # ps = ax[i].plot_surface(X0, Y0, posterior_probability(val, X0, Y0),
    #                         cmap='viridis', vmin=0, vmax=1,  rstride=5, cstride=5)
    # f.colorbar(ps, ax=ax[i], shrink=0.75, location='bottom')

    ax[i].plot_wireframe(X0, Y0, posterior_probability(val, X0, Y0), 
                         color='k', rstride=5, cstride=5)
    ax[i].set_title('Initial POS: {}'.format(val))
    ax[i].set_xlabel('Sensitivity')
    ax[i].set_ylabel('Specificity')
    ax[i].set_zlabel('Posterior POS')
#    ax[0].view_init(15, -37)
#    ax[1].view_init(80, -90)



#--- make some noise
rng = np.random.default_rng(42)
samples = 200

noise = rng.uniform(low=0.00, high=0.02, size=samples)
p0 = rng.normal(loc=0.8, scale=.1, size=samples)
p1 = rng.normal(loc=0.6, scale=.1, size=samples)
p2 = rng.normal(loc=0.9, scale=.05, size=samples)
prior = p0*p1*p2

f, ax = plt.subplots(nrows=4, sharex=True)
# f, ax = plt.subplots(nrows=5, sharex=True)
ax[0].hist(p0)
ax[1].hist(p1)
ax[2].hist(p2)
ax[3].hist(ptot)
# ax[4].hist(noise)
ax[0].set_xlim(0, 1)

# f, ax = plt.subplots()
# ax.hist(noise)


# acc = 0.5 * noise.reshape(1, -1)
# jj = prior.reshape(-1, 1) @ acc

colr = ['k', 'r', 'g']
f, ax = plt.subplots(constrained_layout=True)
for i, val in enumerate([0.5, 0.7, 0.9]):
    ax.plot(prior, posterior_probability(prior, val+noise, val+noise), marker='.', ls='none', alpha=0.2, color=colr[i], label='Sens=Spec={}'.format(val))
ax.set_xlim(0, 1.1)
ax.set_ylim(0, 1.1)
ax.grid()
ax.set_xlabel('Prior Probability P(H)')
ax.set_ylabel('Posterior Probability P(H|A)')
# ax.set_title('Sensitivity: {}, Specificity: {}'.format(sens, spec))

f, ax = plt.subplots(nrows=3, sharex=True, constrained_layout=True)
for i, val in enumerate([0.5, 0.7, 0.9]):
    ax[i].hist(posterior_probability(prior, val+noise, val+noise), color=colr[i])
    ax[i].set_title('Sens=Spec={}'.format(val))
ax[2].set_xlabel('Posterior Probability P(H|A)')
ax[0].set_xlim(0, 1)


