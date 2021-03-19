import random, math, pylab

def psi_0_sq(x):
	psi_0 = math.pi**(-1/4) * math.exp( - x**2 / 2)
	return psi_0*psi_0

x = 0.0
delta = 0.5
data = []
n_steps=50000
for k in range(n_steps):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  psi_0_sq(x_new)/psi_0_sq(x): 
        x = x_new 
    data.append(x)

pylab.hist(data, 100, density = 'True',label='Normalized Histogram')
x = pylab.arange(-3,3,0.01)
y = [psi_0_sq(a) for a in x]
pylab.plot(x, y, c='red', alpha=0.85, linewidth=2.0,label=r'$|\psi_o(x)|^2$')
pylab.title('Theoretical distribution and histogram for '+str(len(data))+' samples')
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$')
pylab.legend()
pylab.savefig('plot_markov_harmonic.png',dpi=300)