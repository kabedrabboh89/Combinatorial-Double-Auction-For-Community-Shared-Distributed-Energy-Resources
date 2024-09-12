import pandas as pd
import numpy as np
from utility import disutility
from time import time
import random
import math
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

for t in range(24):
    demand_bids = np.zeros(100)
    i = 0
    for buyer in consumer:
        demand_bids[i] = consumption[buyer][t]
        i += 1
    upper_price = math.floor(grid_price[t]*1000)
    demand_price = [random.randrange(55, upper_price)/1000 for _ in range(100)]
    demand_price = demand_price
    demand_dict = {'id': consumer, 'price': demand_price, 'quantity': demand_bids}

    supply_bids = np.zeros(6)
    supply_price = np.zeros(6)
    supply_id = range(1, 7)
    for j in range(6):
        if j == 0:
            supply_bids[j] = ders['s1_der1_cap'][t]
            supply_price[j] = ders['s1_der1_pi'][t]
        if j == 1:
            supply_bids[j] = ders['s1_der2_cap'][t]
            supply_price[j] = ders['s1_der2_pi'][t]
        if j == 2:
            supply_bids[j] = ders['s2_der1_cap'][t]
            supply_price[j] = ders['s2_der1_pi'][t]
        if j == 3:
            supply_bids[j] = ders['s2_der2_cap'][t]
            supply_price[j] = ders['s2_der2_pi'][t]
        if j == 4:
            supply_bids[j] = ders['s3_der1_cap'][t]
            supply_price[j] = ders['s3_der1_pi'][t]
        if j == 5:
            supply_bids[j] = ders['s3_der2_cap'][t]
            supply_price[j] = ders['s3_der2_pi'][t]
    supply_dict = {'id': supply_id, 'price': supply_price, 'quantity': supply_bids}

    demand = pd.DataFrame.from_dict(demand_dict)
    demand.sort_values('price', axis=0, ascending=False, inplace=True, ignore_index=True)
    supply = pd.DataFrame.from_dict(supply_dict)
    supply.sort_values('price', axis=0, ascending=True, inplace=True, ignore_index=True)
    # print(demand)
    # print(supply)
    condition = 0
    demand_q = 0
    supply_q = 0
    k = 0
    l = 0
    while condition == 0:
        if demand['price'][k] > supply['price'][l]:
            for i in range(k+1):
                demand_q += demand['quantity'][i]
            for j in range(l+1):
                supply_q += supply['quantity'][j]
            if demand_q < supply_q:
                k += 1
                continue
            else:
                l += 1
        else:
            condition = 1
    print('k = ', k)
    print('l = ', l)
    if k > 0:
        clearing_price = (demand['price'][k-1] + supply['price'][l])/2
    print(clearing_price)
    double = pd.read_csv('./DA.csv')
    double.at[t, 'clearing_price'] = clearing_price
    for i in range(6):
        if clearing_price > supply['price'][i]:
            y = supply['id'][i]
            double.at[t, str(y)] = min(supply['quantity'][i], supply_q)

    df = pd.DataFrame(double)
    df.to_csv('./DA.csv', index=False)



