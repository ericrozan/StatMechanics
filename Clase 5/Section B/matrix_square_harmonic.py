import math, numpy, pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

def pi_quant(x,beta):
	tanh=math.tanh(beta/2.0)
	return math.sqrt(tanh/math.pi) * math.exp(-x**2.0*tanh) 

x_max = 5.0
nx = 100
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-int((nx - 1) / 2), int(nx / 2 + 1))] 
beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
beta     = 2.0 ** (2)                      # actual value of beta (power of 2)
rho = rho_harmonic_trotter(x, beta_tmp)  # density matrix at initial beta
while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0


Z = sum(rho[j, j] for j in range(len(rho[0]))) * dx
pi_of_x = [rho[j, j] / Z for j in range(len(rho[0]))]
f = open('data_harm_matrixsquaring_beta' + str(beta) + '.dat', 'w')
for j in range(len(rho[0])):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

pylab.plot(x,pi_of_x,lw=4,label='Matrix squaring')
pi_quant=[pi_quant(a,beta) for a in x]
pylab.plot(x,pi_quant,lw=1.5,label='Exact quantum solution')

pylab.legend()
pylab.title(r'Matrix squaring and theoretical solutions for $\beta$='+str(beta))
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$')
pylab.savefig('harm_matrixsquaring_beta' + str(beta) + '.png',dpi=300)
