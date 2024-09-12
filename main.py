import pandas as pd
import numpy as np
from utility import disutility
from time import time
import importlib
start = time()


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
m = len(ders['der'])
nodes_j = ders['node']


####  Auction  ####

## collecting bids from DERs ##

## capacities (C_jk) ##

capacity = {'11': ders['s1_der1_cap'], '12': ders['s1_der2_cap'], '21': ders['s2_der1_cap'], '22': ders['s2_der2_cap'],
            '31': ders['s3_der1_cap'], '32': ders['s3_der2_cap']}

## price (pi_jk) ##

prices = {'11': ders['s1_der1_pi'], '12': ders['s1_der2_pi'], '21': ders['s2_der1_pi'], '22': ders['s2_der2_pi'],
          '31': ders['s3_der1_pi'], '32': ders['s3_der2_pi']}

## emf (e_jk) ##

emf = {'11': ders['s1_der1_emf'], '12': ders['s1_der2_emf'], '21': ders['s2_der1_emf'], '22': ders['s2_der2_emf'],
          '31': ders['s3_der1_emf'], '32': ders['s3_der2_emf']}


####  Collecting bids from consumers  #### disutility(demand_i, node_i, gamma_i, pi_g, e_g, node_j, k_j, pi_j, e_j)

bids = {}
i = 0
counter = 0
for buyer in consumer:
    i += 1
    node_i = nodes_i[i - 1]
    gamma_i = gammas[i - 1]/1000
    for j in range(3):
        node_j = nodes_j[j]
        bid_identifier = 'bid_' + str(i) + str(j+1)
        bids[bid_identifier] = []
        for t in range(time_steps):
            demand_it = consumption[buyer][t]
            pi_gt = grid_price[t]
            e_gt = grid_emf[t]
            pi_j = [prices[str(j+1)+'1'][t], prices[str(j+1)+'2'][t]]
            e_j = [emf[str(j+1)+'1'][t], emf[str(j+1)+'2'][t]]
            bids[bid_identifier] += disutility(demand_it, node_i, gamma_i, pi_gt, e_gt, node_j, 2, pi_j, e_j)
            counter += 1
            #print(counter, '  /', n*3*time_steps)
            # print('consumer:', str(i))
            # print('der:', str(j+1))
            # print('time step:', str(t+1))
            # print('####################################')

df1 = pd.DataFrame(bids)
df1.to_csv('./bids.csv', index=False)

print(f'time: {time() - start} seconds')

importlib.import_module('SWO')
# importlib.import_module('post_processing')

#print(f'time: {time() - start} seconds')

