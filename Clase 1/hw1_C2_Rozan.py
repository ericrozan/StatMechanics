import random, math
n_trials = 400000
n_hits = 0
var = 0.0
sum_obs=0.0
sum_obs2=0.0
for iter in range(n_trials):
    x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    Obs = 0.0
    Obs2=0.0
    if x**2 + y**2 < 1.0:
        n_hits += 1
        Obs = 4.0
        Obs2=16.0

    sum_obs+=Obs
    sum_obs2+=Obs2
    

mean_obs=sum_obs/n_trials
mean_obs2=sum_obs2/n_trials

var=mean_obs2-mean_obs**2
std=math.sqrt(var)


print('pi estimate | <obs2> | variance | deviation\n %7.6f   | %6.4f| %6.4f   | %6.4f'%( mean_obs, mean_obs2, var, std))