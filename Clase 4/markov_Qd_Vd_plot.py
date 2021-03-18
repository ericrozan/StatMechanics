import random, math, pylab

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

def Q_d(d):
	return V_sph(d)/V_sph(d-1)
d_max=201
delta = 0.1
n_trials = 10**4
Q_vector=[2]
V_vector=[2]

for d in range(2,d_max):
	x=[0.0]*(d-1)
	old_radius_square=0.0
	n_hits = 0

	for i in range(n_trials):
		k = random.randint(0, d - 2)
		x_old_k = x[k]
		x_new_k = x_old_k + random.uniform(-delta, delta)
		new_radius_square = old_radius_square + x_new_k ** 2 - x_old_k ** 2
		if new_radius_square < 1.0:
			x[k] = x_new_k
			old_radius_square = new_radius_square
		alpha = random.uniform(-1.0, 1.0)
		if old_radius_square + alpha**2 < 1.0: n_hits += 1

	Q_vector+=[2 * n_hits / float(n_trials)]
	V_vector+=[V_vector[len(V_vector)-1]*Q_vector[len(Q_vector)-1]]
	
d_range=range(1,d_max)
exact_volumes=[V_sph(dimension) for dimension in d_range]
pylab.plot(d_range,exact_volumes,label='Exact volumes',lw=3.5)
pylab.plot(d_range,V_vector,label='Sampled volumes')
pylab.yscale('log')
pylab.legend()
pylab.xlabel('Dimensions')
pylab.ylabel('Unit sphere volume')
pylab.title('Sampled and exact sphere volumes')
pylab.savefig('sphere_volumes_plot.png')