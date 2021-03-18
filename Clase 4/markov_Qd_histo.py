import random, math, pylab

d=20
x=[0.0]*(d)
radius_square=[0.0]

delta = 0.1
n_trials = 10**6
n_hits = 0
for i in range(n_trials):
	k = random.randint(0, d - 1)
	x_old_k = x[k]
	x_new_k = x_old_k + random.uniform(-delta, delta)
	new_radius_square = radius_square[len(radius_square)-1] + x_new_k ** 2 - x_old_k ** 2
	if new_radius_square < 1.0:
		x[k] = x_new_k
		radius_square+= [new_radius_square]
	alpha = random.uniform(-1.0, 1.0)
	if radius_square[len(radius_square)-1] + alpha**2 < 1.0: n_hits += 1
#print ('<Q_d=%d>='%(d+1),2 * n_hits / float(n_trials))

radius=[math.sqrt(rsquared) for rsquared in radius_square]
pylab.hist(radius, bins=100, density=True, color='r', histtype='step', label='sampled')
r=pylab.arange(0,1,0.01)
P=float(d)*r**(d-1)
pylab.plot(r,P, label=r'Analytic = %d $r^{%d}$'%(d,d-1))
pylab.legend()
pylab.xlabel(r'$r$')
pylab.ylabel(r'$\pi(r)$')
pylab.title('Radius histogram for d=%d'%(d))
pylab.savefig('radius_histogram_d%d.png'%(d))