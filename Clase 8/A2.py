import random, math, os, pylab

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

############## PARAMETERS ###########
L = 128
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}
T = 1.0

############## INITIAL CONFIGURATION ###############
filename = 'data_local_L'+ str(L) + '_T' + str(T) + '.txt'
if os.path.isfile(filename):
    f = open(filename, 'r')
    S = []
    for line in f:
        S.append(int(line))
    f.close()
    print('Starting from file', filename)
else:
    S = [random.choice([1, -1]) for k in range(N)]
    print('Starting from a random configuration')

############## RUN ###############
nsteps = N*3000
beta = 1.0 / T
Energy = energy(S, N, nbr)
E = []

for step in range(nsteps):
    k = random.randint(0, N - 1)
    delta_E = 2.0 * S[k] * sum(S[nn] for nn in nbr[k])
    if random.uniform(0.0, 1.0) < math.exp(-beta * delta_E):
        S[k] *= -1
        Energy += delta_E
    E.append(Energy)
print('mean energy per spin:', sum(E) / float(len(E) * N))

############## SAVE CONFIGURATION #############
f = open(filename, 'w')
for a in S:
   f.write(str(a) + '\n')
f.close()

############## PLOT #############
def x_y(k, L):
    y = k // L
    x = k - y * L
    return x, y

conf = [[0 for x in range(L)] for y in range(L)]
for k in range(N):
    x, y = x_y(k, L)
    conf[x][y] = S[k]

pylab.imshow(conf, extent=[0, L, 0, L], interpolation='nearest')
pylab.set_cmap('hot')
pylab.title('Local T='+ str(T) + 'L=' + str(L) + 't=5000*N')
pylab.xlabel(r'$x$')
pylab.ylabel(r'$y$')

pylab.savefig('plot_A2_local_T'+ str(T) + '_L' + str(L)+ '.png')
