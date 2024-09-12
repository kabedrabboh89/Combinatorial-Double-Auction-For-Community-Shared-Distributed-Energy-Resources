import pandas as pd
import numpy as np
import cvxpy as cp
from time import time



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
consumers = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

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

n=5000

u = np.zeros((24, n, 3), dtype=float)
d = np.zeros((24, n, 3, 2), dtype=float)
pi = np.zeros((24, 3, 2), dtype=float)
c = np.zeros((24, 3, 2), dtype=float)

t=14
for i in range(1, 101):
    for j in range(1, 4):
        u[t-1][i-1][j-1] = uti(t, i, j)
        for k in range(1, 3):
            d[t-1][i-1][j-1][k-1] = dem(t, i, j, k)
for j in range(1, 4):
    for k in range(1, 3):
        pi[t-1][j-1][k-1] = pai(t, j, k)
        c[t-1][j-1][k-1] = cap(t, j, k)




for i in range(101, n+1):
    for j in range(1, 4):
        u[t-1][i-1][j-1] = np.random.randint(90, high=110)/100 * u[t-1][i-101][j-1]
        for k in range(1, 3):
            d[t-1][i-1][j-1][k-1] = np.random.randint(90, high=110)/100 * d[t-1][i-101][j-1][k-1]



start = time()
#####  SOCIAL WELFARE OPT  #####
print(f'time: {time() - start} seconds')

t=14
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

print(f'time: {time() - start} seconds')







