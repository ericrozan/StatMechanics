import random
import math

def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)

def Q_d(d):
	return V_sph(d)/V_sph(d-1)

delta = 0.1
n_trials = 10**6
Q_vector=[2]
V_vector=[2]

for d in range(2,201):
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
	
	if d in [4,200]:
		print('Estimated Q_%d='%(d),Q_vector[len(Q_vector)-1])
		print('Exact Q_%d='%(d), Q_d(d))
		print('Estimated V_%d='%(d),V_vector[len(V_vector)-1])
		print('Exact V_%d='%(d), V_sph(d),'\n')