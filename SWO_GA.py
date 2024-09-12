import pandas as pd
import numpy as np
from time import time
from geneticalgorithm import geneticalgorithm as ga
start = time()


####  initialisation  ####

####  consumers  ####

consumers = pd.read_csv('./data/consumers.csv')

consumer = consumers['consumer']

n = len(consumer)

####  DERs  ####

ders = pd.read_csv('./data/der.csv')

time_steps = len(ders['hour'])
m = 3

#####  parameters  #####


def u(t, i, j):
    bids = pd.read_csv('./bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3
    return bids[bid_identifier][tao]


def d(t, i, j, k):
    bids = pd.read_csv('./bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3 + k
    return bids[bid_identifier][tao]


def pi(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    pi_identifier = 's' + str(j) + '_der' + str(k) + '_pi'
    tao = t - 1
    return ders[pi_identifier][tao]


def c(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    pi_identifier = 's' + str(j) + '_der' + str(k) + '_cap'
    tao = t - 1
    return ders[pi_identifier][tao]


#####  SOCIAL WELFARE OPT  #####
results = {}

t = 1
x_index = 0
fitness_fnc = np.zeros(300)
for i in range(1, 101):
    for j in range(1, 4):
        fitness_fnc[x_index] = (u(t, i, j) + d(t, i, j, 1) * pi(t, j, 1) + d(t, i, j, 2) * pi(t, j, 2))
        x_index += 1

def f(X):
    pen = 0
    for i in range(1, n + 1):
        x_index = i * 3 - 3
        if X[x_index] + X[x_index + 1] + X[x_index + 2] > 1:
            pen += 10000
        # for j in range(1, 4):
        #     for k in range(1, 3):
        #         sum_djk = 0
        #         for i in range(1, 101):
        #             x_index = i * 3 - 4 + j
        #             sum_djk += d(1, i, j, k) * X[x_index]
        #         cap = c(1, j, k)
        #         if sum_djk > cap:
        #             pen += 10000
    return -1 * np.dot(fitness_fnc, X) + pen


algorithm_param = {'max_num_iteration': 5000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': 1000}

model=ga(function=f,dimension=300,variable_type='bool', algorithm_parameters=algorithm_param)
model.run()

#results[str(t)][0] = social_welfare
#results[str(t)] = x.value
#print(t)
#print(social_welfare)
# df = pd.DataFrame(results)
# df.to_csv('./results.csv', index=False)
print(f'time: {time() - start} seconds')

