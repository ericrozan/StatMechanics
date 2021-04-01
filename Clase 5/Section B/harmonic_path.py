import math, random,pylab

def rho_free(x, y, beta):    # free off-diagonal density matrix
		return math.exp(-(x - y) ** 2 / (2.0 * beta)) 

def read_file(filename):
    list_x = []
    list_y = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            list_x.append(float(x))
            list_y.append(float(y))
    f.close()
    return list_x, list_y

beta = 4.0
N = 10                                            # number of slices
dtau = beta / N
delta = 1.0                                       # maximum displacement on one slice
n_steps = 1000000                                 # number of Monte Carlo steps
x = [0.0] * N 																		# initial path
x_index=0
data=[] 

for step in range(n_steps):
	k = random.randint(0, N - 1)                  # random slice
	knext, kprev = (k + 1) % N, (k - 1) % N       # next/previous slices
	x_new = x[k] + random.uniform(-delta, delta)  # new position at slice k
	old_weight  = (rho_free(x[knext], x[k], dtau) * rho_free(x[k], x[kprev], dtau) *
		math.exp(-0.5 * dtau * x[k] ** 2))
	new_weight  = (rho_free(x[knext], x_new, dtau) * rho_free(x_new, x[kprev], dtau) *
		math.exp(-0.5 * dtau * x_new ** 2))
	if random.uniform(0.0, 1.0) < new_weight / old_weight:
		x[k] = x_new
	if step % 10 == 0:
		data+=[x[x_index]]



pylab.hist(data, 100, density = 'True',label='Normalized Histogram')
filename='data_harm_matrixsquaring_beta' + str(beta) + '.dat'
x_plot,pi_matrix=read_file(filename)
pylab.plot(x_plot,pi_matrix,lw=2,alpha=0.75,label='Matrix squaring result')
pylab.legend()
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$')
pylab.xlim(-2.0, 2.0)
pylab.title(r'Histogram of $x_{%d}$ for N=%d $\beta$='%(x_index,N) + str(beta))
figname='harmonic_path_beta' + str(beta) + '_N'+str(N) + '_x'+str(x_index) +'.png'
pylab.savefig(figname,dpi=300)