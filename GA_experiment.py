import pandas as pd
import numpy as np
from time import time
import cvxpy as cp
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

# def f(X):
#     return np.sum(X)
#
#
# model=ga(function=f,dimension=30,variable_type='bool')
#
# model.run()
def f(X):
    fitness_fnc = 0
    for i in range(1, n + 1):
        x_index = i * 3 - 3
        fitness_fnc += ((x[x_index] + x[x_index+1] + x[x_index+2]) - 1) * -1000
    for j in range(1, m+1):
        for k in range(1, 3):
            sum_djk = 0
            for i in range(1, n + 1):
                x_index = i * 3 - 4 + j
                sum_djk += d(t, i, j, k) * x[x_index]
            cap = c(t, j, k)
            fitness_fnc += (sum_djk - cap) * -10000
    return np.dot(fitness_fnc, X)
# algorithm_param = {'max_num_iteration': 3000,
#                    'population_size': 100,
#                    'mutation_probability': 0.1,
#                    'elit_ratio': 0.01,
#                    'crossover_probability': 0.5,
#                    'parents_portion': 0.3,
#                    'crossover_type': 'uniform',
#                    'max_iteration_without_improv': None}
# model=ga(function=f,dimension=300,variable_type='bool')
# model.run()

X = cp.Variable(300)
print(f(X))

print(f'time: {time() - start} seconds')

