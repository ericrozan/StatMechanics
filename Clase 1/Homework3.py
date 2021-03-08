import random
import pylab as py

def markov_pi(N, delta):
    x, y = 1.0, 1.0
    n_hits = 0
    for i in range(N):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
        if x**2 + y**2 < 1.0: n_hits += 1
    return n_hits


n_runs = 500
for delta in [0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0]:
    n_trials_list = []
    sigmas = []
    pi_list=[]
    poweroftwo_list=[]
    for poweroftwo in range(4, 13):
        n_trials = 2 ** poweroftwo
        sigma = 0.0
        for run in range(n_runs):
            pi_est = 4.0 * markov_pi(n_trials, delta) / float(n_trials)
            sigma += (pi_est - py.pi) ** 2
        sigmas.append(py.sqrt(sigma/(n_runs)))
        n_trials_list.append(n_trials)
        pi_list+=[pi_est]
        poweroftwo_list+=[poweroftwo]
    #py.plot(n_trials_list, sigmas, 'o', ms = 8, label = r'$\delta = $' + str(delta))
    py.plot(poweroftwo_list,pi_list,'.',ms=5,label = r'$\delta = $' + str(delta))
'''
py.plot([10.0, 10000.0], [1.642 / py.sqrt(10.0), 1.642 / py.sqrt(10000.0)],lw=2,color='k', label = 'Direct')
py.xscale('log')
py.yscale('log')
py.xlabel('number of trials')
py.ylabel('root mean square deviation')
py.legend(loc='upper right')
py.title('Markov-chain sampling of pi: root mean square deviation vs. n_trials')
py.savefig('markov_sampling_rms_deviation.png',dpi=300)
'''
py.legend(loc='upper right')
py.axhline(y=py.pi,lw=1,color='k')
py.xlabel(r'$\log_2$(number of trials)')
py.ylabel(r'$\pi$ estimation')
py.savefig('pi_estimation_markov.png',dpi=300)
