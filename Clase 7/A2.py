import math, random, pylab

def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

def pi_two_bosons(x, beta):
    pi_x_1 = math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta / 2.0))
    pi_x_2 = math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
             math.exp(-x ** 2 * math.tanh(beta))
    weight_1 = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    weight_2 = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))
    pi_x = pi_x_1 * weight_1 + pi_x_2 * weight_2
    return pi_x

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)

def run(beta): #This is the original script
    low = levy_harmonic_path(2)
    high = low[:]
    one_cycle=0
    two_cycles=0

    for step in range(nsteps):
        # move 1
        if low[0] == high[0]:
            k = random.choice([0, 1])
            low[k] = levy_harmonic_path(1)[0]
            high[k] = low[k]
            two_cycles+=1
        else:
            low[0], low[1] = levy_harmonic_path(2)
            high[1] = low[0]
            high[0] = low[1]
            one_cycle+=1
        # move 2
        weight_old = (rho_harm_1d(low[0], high[0], beta) *
                      rho_harm_1d(low[1], high[1], beta))
        weight_new = (rho_harm_1d(low[0], high[1], beta) *
                      rho_harm_1d(low[1], high[0], beta))
        if random.uniform(0.0, 1.0) < weight_new / weight_old:
            high[0], high[1] = high[1], high[0]

    return one_cycle,two_cycles

nsteps = 1000
beta_list = pylab.arange(0.1,5,0.1)
pi_one_cycle=[]
pi_two_cycles=[]

for beta in beta_list:
    one_cycle,two_cycles=run(beta)
    #Remember that  one_cycle + two_cycles = nsteps
    pi_one_cycle+=[one_cycle/nsteps]
    pi_two_cycles+=[two_cycles/nsteps]

fract_two_cycles = [z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta)) for beta in beta_list]
fract_one_cycle = [z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta)) for beta in beta_list]

pylab.plot(beta_list,fract_one_cycle, lw=3,c='C0',alpha=0.7, label='Analytical fract. 1 cycle')
pylab.plot(beta_list,pi_one_cycle, '.', label='Sampled fract. 1 cycle',c='C0',mec='k',ms=7)

pylab.plot(beta_list,fract_two_cycles, lw=3,c='C1',alpha=0.7, label='Analytical fract. 1 cycle')
pylab.plot(beta_list,pi_two_cycles, '.',label='Sampled fract. 2 cycle',c='C1',mec='k',ms=7)




pylab.xlabel(r'Inverse temperature $\beta$')
pylab.ylabel(r'Probability')
pylab.title(r'One and two cycles probability')
pylab.legend()
pylab.savefig('A2_cont.png',dpi=300)