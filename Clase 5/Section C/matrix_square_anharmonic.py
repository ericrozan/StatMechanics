import math, numpy, pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

def V(x, cubic, quartic):
    return 0.5 * x** 2 + cubic * x** 3 + quartic * x** 4

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_anharmonic_trotter(grid, beta, cubic, quartic):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * ( V(x, cubic, quartic) + V(xp, cubic, quartic))) \
                         for x in grid] for xp in grid])

def pi_quant(x,beta):
    tanh=math.tanh(beta/2.0)
    return math.sqrt(tanh/math.pi) * math.exp(-x**2.0*tanh) 

x_max = 5.0
nx = 1000
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-int((nx - 1) / 2), int(nx / 2 + 1))] 
cubic = -1.0
quartic = 1.0


beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
beta     = 2.0 ** (2)                      # actual value of beta (power of 2)
rho = rho_anharmonic_trotter(x, beta_tmp, cubic, quartic)  # density matrix at initial beta
while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0


Z = sum(rho[j, j] for j in range(len(rho[0]))) * dx
pi_of_x = [rho[j, j] / Z for j in range(len(rho[0]))]
f = open('data_anharmonic_matrixsquaring_beta' + str(beta) + '.dat', 'w')
for j in range(len(rho[0])):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

pylab.plot(x,pi_of_x,lw=2,label='Anharmonic solution')
pi_quant=[pi_quant(a,beta) for a in x]
pylab.plot(x,pi_quant,lw=2,label='Harmonic solution')

pylab.legend()
pylab.title(r'Matrix squaring solution for $\beta$='+str(beta))
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$')
pylab.savefig('Anharm_matrixsquaring_beta' + str(beta) + '.png',dpi=300)
