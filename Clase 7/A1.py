import math, random, pylab


def pi_x(x, beta):
	sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
	pi=math.exp(-x ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi*sigma)
	return pi

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
high = low[:]
data = []
for step in range(nsteps):
	k = random.choice([0, 1])
	low[k] = levy_harmonic_path(1)[0]
	high[k] = low[k]
	data+=high


pylab.hist(data, density=True, bins=100, label='Sampled Histogram')
x_plot=pylab.arange(-3,3,0.01)
y_plot=[pi_x(a,beta) for a in x_plot]
pylab.plot(x_plot,y_plot, lw=2, label='Analytic solution')
pylab.xlabel('x')
pylab.ylabel(r'$\pi(x)$')
pylab.title(r'Probability distribution of particles, $\beta=%s$'%(beta))
pylab.legend()
pylab.savefig('A1.png')