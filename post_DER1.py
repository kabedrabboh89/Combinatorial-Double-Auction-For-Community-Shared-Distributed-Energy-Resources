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

ders = pd.read_csv('./data/der.csv')


time_steps = len(ders['hour'])
m = 3
nodes_j = ders['node']


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
    c_identifier = 's' + str(j) + '_der' + str(k) + '_cap'
    tao = t - 1
    return ders[c_identifier][tao]

def emf(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    emf_identifier = 's' + str(j) + '_der' + str(k) + '_emf'
    tao = t - 1
    return ders[emf_identifier][tao]



charging_grid = ders['charging_grid']
charging_re = ders['charging_RE']


results = pd.read_csv('./results.csv')

#####  CALCULATIONS  #####

post = pd.read_csv('./post_DER.csv')

post['charging_grid'] = charging_grid
post['charging_RE'] = charging_re

for t in range(1, time_steps+1):
    print(t)
    x = results[str(t)]
    x_index = 0
    j=1
    revenue_j = 0
    for k in range(1, 3):
        identifier = 'der' + str(j) + str(k)
        sum_djk = 0
        for i in range(1, n + 1):
            x_index = i * 3 - 4 + j
            sum_djk += d(t, i, j, k) * x[x_index]
        post.at[t-1, identifier] = sum_djk
        pijk = pi(t, j, k)
        pi_identifier = 'pi' + str(j) + str(k)
        post.at[t - 1, pi_identifier] = pijk
        revenue_j += sum_djk * pijk
    revenue_j -= charging_grid[t-1] * grid_price[t-1]
    revenue_identifier = 'revenue_der' + str(j)
    post.at[t-1, revenue_identifier] = revenue_j

    # total_100_der = 0
    # total_100_losses = 0
    # total_100_grid = 0
    # total_100_ei = 0
    # for i in range(1, n + 1):
    #     print(t, '  /24   ', i, '   /100')
    #     x_index = i * 3 - 3
    #     demand_ij = x[x_index] * (d(t, i, 1, 1) + d(t, i, 1, 2)) + x[x_index+1] * (d(t, i, 2, 1) + d(t, i, 2, 2))\
    #                 + x[x_index+2] * (d(t, i, 3, 1) + d(t, i, 3, 2))
    #     losses_ij = (d(t, i, 1, 1) + d(t, i, 1, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[0]) * x[x_index]\
    #                 + (d(t, i, 2, 1) + d(t, i, 2, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[1]) * x[x_index+1]\
    #                 + (d(t, i, 3, 1) + d(t, i, 3, 2))**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[2]) * x[x_index+2]
    #     demand_ig = consumption[consumer[i-1]][t-1] - demand_ij + losses_ij
    #     ei_i = x[x_index] * (d(t, i, 1, 1) * emf(t, 1, 1) + d(t, i, 1, 2) * emf(t, 1, 2)) + \
    #            x[x_index+1] * (d(t, i, 2, 1) * emf(t, 2, 1) + d(t, i, 2, 2) * emf(t, 2, 2)) +\
    #              x[x_index+2] * (d(t, i, 3, 1) * emf(t, 3, 1) + d(t, i, 3, 2) * emf(t, 3, 2)) + \
    #            demand_ig * grid_emf[t-1]
    #     total_100_der += demand_ij
    #     total_100_losses += losses_ij *1000
    #     total_100_grid += demand_ig
    #     total_100_ei += ei_i
    # post.at[t-1, 'total_100_der'] = total_100_der
    # post.at[t-1, 'total_100_losses'] = total_100_losses
    # post.at[t-1, 'total_100_grid'] = total_100_grid
    # post.at[t - 1, 'total_100_ei'] = total_100_ei


df = pd.DataFrame(post)
df.to_csv('./post_DER1.csv', index=False)
print(f'time: {time() - start} seconds')






