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

def Energy_pert(n, cubic, quartic):
    return n + 0.5 - 15.0 / 4.0 * cubic **2 * (n ** 2 + n + 11.0 / 30.0) \
         + 3.0 / 2.0 * quartic * (n ** 2 + n + 1.0 / 2.0)

def Z_pert(cubic, quartic, beta, n_max):
    Z = sum(math.exp(-beta * Energy_pert(n, cubic, quartic)) for n in range(n_max + 1))
    return Z

def pi_quant(x,beta):
    tanh=math.tanh(beta/2.0)
    return math.sqrt(tanh/math.pi) * math.exp(-x**2.0*tanh) 

x_max = 5.0
n_max=20
nx = 1000
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-int((nx - 1) / 2), int(nx / 2 + 1))] 

epsilon_list= [0.001,0.01,0.1,0.2,0.3,0.4,0.5] #As required for section C3

table=open('Z_table.txt', 'w')
table.write('quadric | Z | Z_pert\n')

for epsilon in epsilon_list:
    cubic = -epsilon
    quartic = epsilon

    beta_tmp = 2.0 ** (-8)                   # initial value of beta (power of 2)
    beta     = 2.0 
    rho = rho_anharmonic_trotter(x, beta_tmp, cubic, quartic)  # density matrix at initial beta
    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        beta_tmp *= 2.0

    Z = sum(rho[j, j] for j in range(len(rho[0]))) * dx
    pi_of_x = [rho[j, j] / Z for j in range(len(rho[0]))]
    Z_p=Z_pert(cubic, quartic, beta, n_max)
    table.write(str(quartic)+ ' | ' + str(Z) + ' | ' + str(Z_p)+'\n')


table.close()