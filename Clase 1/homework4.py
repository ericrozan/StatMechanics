import random


n_trials = 2**14
delta_list=[0.062, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0]
f= open('homework4_list.txt','w')
#f.write('delta | acceptance | rate\n')
f.write('delta | acceptance rate\n')
for delta in delta_list:
	accepted=0
	x, y = 1.0, 1.0
	n_hits = 0
	for i in range(n_trials):
		del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
		if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
			x, y = x + del_x, y + del_y
			accepted+=1
		if x**2 + y**2 < 1.0:
			n_hits += 1
	#f.write('{:04.3f} | {:4d}  | {} \n'.format(delta,accepted,accepted/n_trials))
	f.write('{:04.3f} | {:6f} \n'.format(delta,accepted/n_trials))
	
f.close()