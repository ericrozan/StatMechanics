import random, math, pylab, os

def dist(x,y):
	d_x = abs(x[0] - y[0]) % 1.0
	d_x = min(d_x, 1.0 - d_x)
	d_y = abs(x[1] - y[1]) % 1.0
	d_y = min(d_y, 1.0 - d_y)
	return  math.sqrt(d_x**2 + d_y**2)


def show_conf(L, sigma, title, fname):
	pylab.axes()
	color_number=0
	for [x, y] in L:
		for ix in range(-1, 2):
			for iy in range(-1, 2):
				#cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='C%d'%(color_number))
				cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
				pylab.gca().add_patch(cir)
		color_number+=1

	pylab.axis('scaled')
	pylab.title(title)
	pylab.axis([0.0, 1.0, 0.0, 1.0])
	pylab.savefig(fname)
	pylab.show()
	pylab.close()

K=10
N=K**2
eta=0.42
sigma_sq = eta/(N*math.pi)
sigma = math.sqrt(sigma_sq)
delta = 0.3*sigma
n_steps = 10000
filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)

two_delxy=1/K
delxy=0.5*two_delxy

if os.path.isfile(filename):
	f = open(filename, 'r')
	L = []
	for line in f:
		a, b = line.split()
		L.append([float(a), float(b)])
	f.close()
	print('starting from file', filename)
else:
	L = [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(K) for j in range(K)]
	print('starting from a new lattice configuration')


for steps in range(n_steps):
	a = random.choice(L)
	b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
	min_dist_sq = min((dist(b,c))** 2 for c in L if c != a)
	if not (min_dist_sq < 4.0 * sigma_sq):
		for k in range(len(b)):
			b[k]=b[k] %1  #If the new position is outside the box, the modulus will fix it
		a[:] = b

f = open(filename, 'w')
for a in L:
   f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
show_conf(L, sigma, 'N=%d Disks in a periodic box'%(N), 'N%d_disks.png'%(N))
