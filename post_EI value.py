import pandas as pd
import numpy as np
from network import Resistance
from time import time
start = time()


####  initialisation  ####
####  initialisation  ####

####  consumers  ####

consumption = pd.read_csv('./data/consumption_data.csv')
consumers = pd.read_csv('./data/consumers.csv')

consumer = consumers['consumer']
nodes_i = consumers['node']
gammas = consumers['gamma']


n = len(consumer)

####  grid  ####

grid_price = consumption['price_grid']
grid_emf = consumption['emf_grid']

####  DERs  ####

ders = pd.read_csv('./data/basic results/der.csv')


time_steps = len(ders['hour'])
m = 3
nodes_j = ders['node']


def u(t, i, j):
    bids = pd.read_csv('./data/basic results/bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3
    return bids[bid_identifier][tao]


def d(t, i, j, k):
    bids = pd.read_csv('./data/basic results/bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3 + k
    return bids[bid_identifier][tao]


def pi(t, j, k):
    ders = pd.read_csv('./data/basic results/der.csv')
    pi_identifier = 's' + str(j) + '_der' + str(k) + '_pi'
    tao = t - 1
    return ders[pi_identifier][tao]


def c(t, j, k):
    ders = pd.read_csv('./data/basic results/der.csv')
    c_identifier = 's' + str(j) + '_der' + str(k) + '_cap'
    tao = t - 1
    return ders[c_identifier][tao]

def emf(t, j, k):
    ders = pd.read_csv('./data/basic results/der.csv')
    emf_identifier = 's' + str(j) + '_der' + str(k) + '_emf'
    tao = t - 1
    return ders[emf_identifier][tao]


results = pd.read_csv('./data/basic results/results.csv')

#####  CALCULATIONS  #####

#post = pd.read_csv('./post.csv')

EI_value=0

for t in range(1, time_steps+1):
    print(t)
    x = results[str(t)]
    x_index = 0
    for i in range(1, n + 1):
        print(t, '  /24   ', i, '   /100')
        x_index = i * 3 - 3
        demand_ij = x[x_index] * (d(t, i, 1, 1) + d(t, i, 1, 2)) + x[x_index+1] * (d(t, i, 2, 1) + d(t, i, 2, 2))\
                    + x[x_index+2] * (d(t, i, 3, 1) + d(t, i, 3, 2))
        losses_ij = (d(t, i, 1, 1) + d(t, i, 1, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[0]) * x[x_index]\
                    + (d(t, i, 2, 1) + d(t, i, 2, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[1]) * x[x_index+1]\
                    + (d(t, i, 3, 1) + d(t, i, 3, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[2]) * x[x_index+2]
        demand_ig = consumption[consumer[i-1]][t-1] - demand_ij + losses_ij * 1000
        ei_i = x[x_index] * (d(t, i, 1, 1) * emf(t, 1, 1) + d(t, i, 1, 2) * emf(t, 1, 2)) + \
                x[x_index+1] * (d(t, i, 2, 1) * emf(t, 2, 1) + d(t, i, 2, 2) * emf(t, 2, 2)) +\
                 x[x_index+2] * (d(t, i, 3, 1) * emf(t, 3, 1) + d(t, i, 3, 2) * emf(t, 3, 2)) + \
                    demand_ig * grid_emf[t-1]
        ei_i_savings = consumption[consumer[i - 1]][t - 1] * grid_emf[t - 1] - ei_i
        EI_value += ei_i_savings * gammas[i-1] /1000


print(EI_value)
print(f'time: {time() - start} seconds')






