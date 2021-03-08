import os, random

filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
if os.path.isfile(filename):
    f = open(filename, 'r')
    L = []
    for line in f:
        a, b = line.split()
        print('a=',a,'b=',b)
        L.append([float(a), float(b)])
    f.close()
    print('starting from file', filename)
else:
    L = [[0.25, 0.25], [0.25, 0.75], [0.75, 0.25], [0.75, 0.75]]
    print('starting from a new random configuration')

L[0][0] = 3.3
f = open(filename, 'w')
for a in L:
   f.write(str(a[0]) + ' ' + str(a[1]) + '\n')
f.close()