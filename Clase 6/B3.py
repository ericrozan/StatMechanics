import math, random, pylab

def rho_free(x, y, beta):
    return math.exp(-(x - y) ** 2 / (2.0 * beta))

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x

beta = 20.0
N = 80
dtau = beta / N
delta = 1.0
n_steps = 4000000
sigma = 1 / math.sqrt(2 * math.tanh(beta/2.0) )
data=[]


for step in range(n_steps):
  if step%(n_steps/100)==0: print('step %i, %i percent'%(step,int(step/n_steps*100)))
  x0 = random.gauss(0.0, sigma)
  x = levy_harmonic_path(x0, x0, dtau, N)
  if step % N == 0:
        k = random.randint(0, N - 1)
        data.append(x[k])



pylab.hist(data, density=True, bins=100, label='QMC')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$ (normalized)')
pylab.title(r'Levy Harmonic Path ($\beta$=%s, N=%i)'%(beta, N))
pylab.xlim(-2, 2)
pylab.savefig('plot_B3_beta%s.png'%(beta))
pylab.clf()

imaginary_time = pylab.arange(0,beta,dtau)
pylab.plot(x,imaginary_time)
pylab.xlabel('x')
pylab.ylabel(r'Imaginary time $\tau$')
pylab.title('Final x configuration of Levy algorithm')
pylab.savefig('B3_path.png')
