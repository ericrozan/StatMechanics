import random

L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
sigma = 0.15
sigma_sq = sigma ** 2
delta = 0.1
n_steps = 10**5
del_xy = 0.05
conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))
configurations = [conf_a, conf_b, conf_c]
hits = {conf_a: 0, conf_b: 0, conf_c: 0}
for steps in range(n_steps):
	a = random.choice(L)
	b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
	min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
	box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
	if not (box_cond or min_dist < 4.0 * sigma_sq):
		a[:] = b
######## I use caps for variables introduced in section A1 to distinguish them from "a" and "b" of this script #########
	for conf in configurations:
			condition_hit = True
			for B in conf:
				condition_B = min(max(abs(A[0] - B[0]), abs(A[1] - B[1])) for A in L) < del_xy
				condition_hit *= condition_B
			if condition_hit:
				hits[conf] += 1

for conf in configurations:
	print(conf, hits[conf])



