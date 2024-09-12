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


def uti(t, i, j):
    bids = pd.read_csv('./bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3
    return bids[bid_identifier][tao]


def dem(t, i, j, k):
    bids = pd.read_csv('./bids.csv')
    bid_identifier = 'bid_' + str(i) + str(j)
    tao = (t-1) * 3 + k
    return bids[bid_identifier][tao]


def pai(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    pi_identifier = 's' + str(j) + '_der' + str(k) + '_pi'
    tao = t - 1
    return ders[pi_identifier][tao]


def cap(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    c_identifier = 's' + str(j) + '_der' + str(k) + '_cap'
    tao = t - 1
    return ders[c_identifier][tao]

def emfi(t, j, k):
    ders = pd.read_csv('./data/der.csv')
    emf_identifier = 's' + str(j) + '_der' + str(k) + '_emf'
    tao = t - 1
    return ders[emf_identifier][tao]

u = np.zeros((24, 100, 3), dtype=float)
d = np.zeros((24, 100, 3, 2), dtype=float)
pi = np.zeros((24, 3, 2), dtype=float)
c = np.zeros((24, 3, 2), dtype=float)
emf = np.zeros((24, 3, 2), dtype=float)

for t in range(1, 25):
    for i in range(1, 101):
        for j in range(1, 4):
            u[t-1][i-1][j-1] = uti(t, i, j)
            for k in range(1, 3):
                d[t-1][i-1][j-1][k-1] = dem(t, i, j, k)
    for j in range(1, 4):
        for k in range(1, 3):
            pi[t-1][j-1][k-1] = pai(t, j, k)
            c[t-1][j-1][k-1] = cap(t, j, k)
            emf[t-1][j-1][k-1] = emfi(t, j, k)


results = pd.read_csv('./results.csv')

#####  CALCULATIONS  #####

post = pd.read_csv('./post.csv')
#demand = pd.read_csv('./demand.csv')

for t in range(1, time_steps+1):
    print(t)
    x = results[str(t)]
    x_index = 0
    for j in range(1, m+1):
        revenue_j = 0
        for k in range(1, 3):
            identifier = 'der' + str(j) + str(k)
            sum_djk = 0
            for i in range(1, n + 1):
                x_index = i * 3 - 4 + j
                sum_djk += d[t-1][i-1][j-1][k-1] * x[x_index]
            post.at[t-1, identifier] = sum_djk
            revenue_j += sum_djk * pi[t-1][j-1][k-1]
        revenue_identifier = 'revenue_der' + str(j)
        post.at[t-1, revenue_identifier] = revenue_j

    total_100_der = 0
    total_100_losses = 0
    total_100_grid = 0
    total_100_ei = 0
    for i in range(1, n + 1):
        print(t, '  /24   ', i, '   /100')
        identifier_grid = str(i)
        identifier_der = 'der' + str(i)
        identifier_losses = 'losses' + str(i)
        x_index = i * 3 - 3
        demand_ij = x[x_index] * (d[t-1][i-1][1-1][1-1] + d[t-1][i-1][1-1][2-1]) + x[x_index+1] * \
                    (d[t-1][i-1][2-1][1-1] + d[t-1][i-1][2-1][2-1])\
                    + x[x_index+2] * (d[t-1][i-1][3-1][1-1] + d[t-1][i-1][3-1][2-1])
        #demand.at[t-1, identifier_der] = demand_ij
        losses_ij = (d[t-1][i-1][1-1][1-1] + d[t-1][i-1][1-1][2-1])**2/(240)**2 * Resistance(nodes_i[i-1], nodes_j[0]) \
                    * x[x_index] + (d[t-1][i-1][2-1][1-1] + d[t-1][i-1][2-1][2-1])**2/(240)**2 \
                    * Resistance(nodes_i[i-1], nodes_j[1]) * x[x_index+1]\
                    + (d[t-1][i-1][3-1][1-1] + d[t-1][i-1][3-1][2-1])**2/(240)**2 * \
                    Resistance(nodes_i[i-1], nodes_j[2]) * x[x_index+2]
        losses_ij *= 1000
        #demand.at[t-1, identifier_losses] = losses_ij *1000
        demand_ig = consumption[consumer[i-1]][t-1] - demand_ij
        #demand.at[t-1, identifier_grid] = demand_ig
        ei_i = x[x_index] * (d[t-1][i-1][1-1][1-1] * emf[t-1][1-1][1-1] + d[t-1][i-1][1-1][2-1] * emf[t-1][1-1][2-1]) +\
               x[x_index+1] * (d[t-1][i-1][2-1][1-1] * emf[t-1][2-1][1-1] + d[t-1][i-1][2-1][2-1] * emf[t-1][2-1][2-1])\
             + x[x_index+2] * (d[t-1][i-1][3-1][1-1] * emf[t-1][3-1][1-1] + d[t-1][i-1][3-1][2-1] * emf[t-1][3-1][2-1]) \
               + demand_ig * grid_emf[t-1]
        total_100_der += demand_ij
        total_100_losses += losses_ij
        total_100_grid += demand_ig
        total_100_ei += ei_i
    post.at[t-1, 'total_100_der'] = total_100_der
    post.at[t-1, 'total_100_losses'] = total_100_losses
    post.at[t-1, 'total_100_grid'] = total_100_grid
    post.at[t - 1, 'total_100_ei'] = total_100_ei


df = pd.DataFrame(post)
df.to_csv('./post.csv', index=False)
print(f'time: {time() - start} seconds')






