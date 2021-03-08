import random, math, pylab, os, cmath

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

##################  NEW FOR EX. C3 ##########################
def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)
#############################################################
#Create a folder for the saved configurations
output_dir='saved_configurations'
if not os.path.exists(output_dir): os.makedirs(output_dir)
startingDir = os.getcwd()
os.chdir(output_dir)

K=10
N=K**2
two_delxy=1/K
delxy=0.5*two_delxy
n_steps = 10000
eta_plot=[]
Psi_mean=[]
Psi_std=[]

#I indent everything from before, and add an extra loop for eta

for eta in pylab.arange(0.05,math.pi/4.0,0.01):
	sigma_sq = eta/(N*math.pi)
	sigma = math.sqrt(sigma_sq)
	delta = 0.3*sigma
	#
	filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
	# I initialize a Psi_vector for each eta, in order to average it at the end.
	Psi_vec=[]

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
				b[k]=b[k] %1  #If the new position is outside the box, the modulus will correct it
			a[:] = b
		if steps%100==0: #Compute Psi_6 every 100 steps
			Psi=Psi_6(L, sigma)
			Psi_vec+=[abs(Psi)]
	f = open(filename, 'w')
	for a in L:
	   f.write(str(a[0]) + ' ' + str(a[1]) + '\n')

	eta_plot+=[eta]
	Psi_mean+=[pylab.mean(Psi_vec)]
	Psi_std+=[pylab.std(Psi_vec)]

pylab.errorbar(eta_plot,Psi_mean,yerr=Psi_std,capsize=3,lw=2,elinewidth=0.5)
pylab.xlabel(r'$\eta$')
pylab.ylabel(r'$\langle \Psi_6 \rangle$')
pylab.title(r'Global order parameter $\Psi_6$ as a function of $\eta$')
os.chdir(startingDir)
pylab.savefig('Global_Order_parameter.png')
pylab.show()
