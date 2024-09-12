import pandas as pd
import numpy as np
import cvxpy as cp
from time import time
from network import Resistance
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
u = np.zeros((24, 100, 3), dtype=float)
d = np.zeros((24, 100, 3, 2), dtype=float)
pi = np.zeros((24, 3, 2), dtype=float)
c = np.zeros((24, 3, 2), dtype=float)
emf = np.zeros((24, 3, 2), dtype=float)

bids = pd.read_csv('./bids.csv')

for t in range(1, 25):
    for i in range(1, 101):
        for j in range(1, 4):
            bid_identifier = 'bid_' + str(i) + str(j)
            tao = (t - 1) * 3
            u[t-1][i-1][j-1] = bids[bid_identifier][tao]
            for k in range(1, 3):
                tao = (t - 1) * 3 + k
                d[t-1][i-1][j-1][k-1] = bids[bid_identifier][tao]
    for j in range(1, 4):
        for k in range(1, 3):
            pi_identifier = 's' + str(j) + '_der' + str(k) + '_pi'
            c_identifier = 's' + str(j) + '_der' + str(k) + '_cap'
            emf_identifier = 's' + str(j) + '_der' + str(k) + '_emf'
            tao = t - 1
            pi[t-1][j-1][k-1] = ders[pi_identifier][tao]
            c[t-1][j-1][k-1] = ders[c_identifier][tao]
            emf[t-1][j-1][k-1] = ders[emf_identifier][tao]


#####  SOCIAL WELFARE OPT  #####
results = {}
optimal_SW = np.zeros(300)

for t in range(1, time_steps+1):
    x = cp.Variable(m*n, boolean=True)
    x_index = 0
    objective_fnc = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            objective_fnc += (u[t-1][i-1][j-1] + d[t-1][i-1][j-1][1-1] * pi[t-1][j-1][1-1] + d[t-1][i-1][j-1][2-1] *
                              pi[t-1][j-1][2-1]) * x[x_index]
            x_index += 1
    constraints = []
    for i in range(1, n + 1):
        x_index = i * 3 - 3
        constraints += [(x[x_index] + x[x_index+1] + x[x_index+2]) <= 1]
    for j in range(1, m+1):
        for k in range(1, 3):
            sum_djk = 0
            for i in range(1, n + 1):
                x_index = i * 3 - 4 + j
                sum_djk += d[t-1][i-1][j-1][k-1] * x[x_index]
            cap = c[t-1][j-1][k-1]
            constraints += [sum_djk <= cap]
    objective = cp.Maximize(objective_fnc)
    prob = cp.Problem(objective, constraints)
    social_welfare = prob.solve(solver=cp.GUROBI, reoptimize=True)
    #results[str(t)][0] = social_welfare
    results[str(t)] = x.value
    optimal_SW[t-1] = social_welfare
    #print(t)
    #print(social_welfare)

results['optimal_SW'] = optimal_SW

df = pd.DataFrame(results)
df.to_csv('./results.csv', index=False)

print('SWO')

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


results = pd.read_csv('./results.csv')

#####  CALCULATIONS  #####

post = pd.read_csv('./post.csv')
#demand = pd.read_csv('./demand.csv')
EI_value = 0
for t in range(1, time_steps+1):
    #print(t)
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
    SW = 0

    for i in range(1, n + 1):
        #print(t, '  /24   ', i, '   /100')
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
        ei_i_savings = consumption[consumer[i - 1]][t - 1] * grid_emf[t - 1] - ei_i
        EI_value += ei_i_savings * gammas[i - 1] / 1000
        u_i = x[x_index] * u[t-1][i-1][1-1] + x[x_index+1] * u[t-1][i-1][2-1] + x[x_index+2] * u[t-1][i-1][3-1]
        total_100_der += demand_ij
        total_100_losses += losses_ij
        total_100_grid += demand_ig
        total_100_ei += ei_i
        SW += u_i
    post.at[t-1, 'total_100_der'] = total_100_der
    post.at[t-1, 'total_100_losses'] = total_100_losses
    post.at[t-1, 'total_100_grid'] = total_100_grid
    post.at[t - 1, 'total_100_ei'] = total_100_ei
    post.at[t - 1, 'SW'] = SW


df = pd.DataFrame(post)
df.to_csv('./post.csv', index=False)

print(f'time: {time() - start} seconds')
print(EI_value)






