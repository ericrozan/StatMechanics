import random
import pylab as py

def direct_pi(N):
    n_hits = 0
    for i in range(N):
        x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
        if x ** 2 + y ** 2 < 1.0:
            n_hits += 1
    return n_hits

n_runs = 500
n_trials_list = []
pi_list=[]
sigmasqs = []
poweroftwo_list=[]
for poweroftwo in range(4, 13):
    n_trials = 2 ** poweroftwo
    sigmasq = 0.0
    for run in range(n_runs):
        pi_est = 4.0 * direct_pi(n_trials) / float(n_trials)
        sigmasq += (pi_est - py.pi) ** 2
    pi_list+=[pi_est]
    sigmasqs.append(py.sqrt(sigmasq/(n_runs)))
    n_trials_list.append(n_trials)
    poweroftwo_list+=[poweroftwo]

py.plot([10.0, 10000.0], [1.642 / py.sqrt(10.0), 1.642 / py.sqrt(10000.0)],lw=2,color='C1')
py.plot(n_trials_list, sigmasqs, 'o-',color='C0')
py.xscale('log')
py.yscale('log')
py.xlabel('number of trials')
py.ylabel('root mean square deviation')
py.title('Direct sampling of pi: root mean square deviation vs. n_trials')
py.savefig('direct_sampling_rms_deviation.png',dpi=300)
#py.show()
py.clf()
py.errorbar(poweroftwo_list,pi_list,yerr=sigmasqs,fmt='.',capsize=5,ms=5)
py.axhline(y=py.pi,lw=1)
py.xlabel(r'$\log_2$(number of trials)')
py.ylabel(r'$\pi$ estimation')
py.savefig('pi_estimation_direct.png',dpi=300)
