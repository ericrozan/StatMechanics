import math, random, pylab

def V_anharm(x, cubic, quartic):
	pot = cubic * x ** 3 + quartic * x ** 4
	return pot


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

def rho_free(x, y, beta):
	return math.exp(-(x - y) ** 2 / (2.0 * beta))


beta = 20
N = 100
dtau = beta / N
delta = 1.0
n_steps = 4000000
x = [0.0] * N
Ncut = int(N/2) #Only going to use it if beta is large
data=[]
Trotter_weight_old = 10**-300 #First move will always be accepted 

quartic = 1
cubic = -quartic


for step in range(n_steps):
	if step%(n_steps/100)==0: print('step %i, %i percent'%(step,int(step/n_steps*100)))
	if beta < 15.0: #For small beta propose an entire new path, for large beta only part of it
		x_new = levy_harmonic_path(x[0], x[0], dtau, N) 
	else:
		x_new = x[Ncut:] + levy_harmonic_path(x[0], x[Ncut], dtau, Ncut) 
	Trotter_weight_new = math.exp(sum(-V_anharm(a, cubic, quartic) * dtau for a in x_new))
	if random.uniform(0.0, 1.0) < Trotter_weight_new / Trotter_weight_old:
		Trotter_weight_old = Trotter_weight_new
		x = x_new[:]
		x = x[1:] + x[:1]	
	if step % 100 == 0:
		k = random.randint(0, N - 1)
		data.append(x[k])



pylab.hist(data, density=True, bins=100, label='Anharmonic Histogram')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
pylab.plot(list_x, list_y, label='Harmonic')
pylab.legend()
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$ (normalized)')
pylab.title(r'Levy Anharmonic Path ($\beta$=%s, N=%i)'%(beta, N))
pylab.xlim(-2, 2)
pylab.savefig('plot_C2_beta%s.png'%(beta))
pylab.clf()

imaginary_time = pylab.arange(0,beta,dtau)
pylab.plot(x,imaginary_time)
pylab.xlabel('x')
pylab.ylabel(r'Imaginary time $\tau$')
pylab.title('Final x configuration of Levy algorithm')
pylab.savefig('C2_path.png')
