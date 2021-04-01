import random, math, pylab

def psi_n_square(x, n):
	if n == -1:
		return 0.0
	else:
		psi = [math.exp(-x ** 2 / 2.0) / math.pi ** 0.25]
		psi.append(math.sqrt(2.0) * x * psi[0])
		for k in range(2, n + 1):
			psi.append(math.sqrt(2.0 / k) * x * psi[k - 1] -
					   math.sqrt((k - 1.0) / k) * psi[k - 2])
		return psi[n] ** 2


def pi_quant(x,beta):
	tanh=math.tanh(beta/2.0)
	return math.sqrt(tanh/math.pi) * math.exp(-x**2.0*tanh) 

def pi_class(x,beta):
	return math.sqrt(beta/ (2.0*math.pi)) * math.exp(-beta*x**2 / 2.0)

x = 0.0
n = 0
delta = 0.5
data = []
n_steps=10**6
beta_selected=[0.2,1,5]

for beta in beta_selected:
	for k in range(n_steps):
		x_new = x + random.uniform(-delta, delta)
		if random.uniform(0.0, 1.0) <  psi_n_square(x_new,n)/psi_n_square(x,n): 
			x = x_new
		m = n + random.choice([-1, 1])
		if random.uniform(0.0, 1.0) <  psi_n_square(x,m)/psi_n_square(x,n) * math.exp( -beta*(m-n) ):
			n = m
		data.append(x)

	pylab.clf()
	pylab.hist(data, 100, density = 'True',label='Normalized Histogram')
	x_limit=max([abs(a) for a in data])+0.5
	x_plot = pylab.arange(-x_limit,x_limit,0.01)
	pi_class_plot = [pi_class(a,beta) for a in x_plot]
	pi_quant_plot = [pi_quant(a,beta) for a in x_plot]
	pylab.plot(x_plot, pi_class_plot, alpha=0.85, linewidth=4,label='Theo. classical probability')
	pylab.plot(x_plot, pi_quant_plot, alpha=0.85, linewidth=2,label='Theo. quantum probability')
	pylab.title(r'Theoretical distributions and histogram for $\beta$='+str(beta))
	pylab.xlabel(r'$x$')
	pylab.ylabel(r'$\pi(x)$')
	pylab.legend()
	figname = 'plot_markov_harmonic_beta' + str(beta) +'.png'
	pylab.savefig(figname,dpi=300)