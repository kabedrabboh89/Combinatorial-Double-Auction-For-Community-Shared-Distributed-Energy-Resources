import pandas as pd
import cvxpy as cp
from network import Resistance
from time import time
start = time()

###  initialisation  ###
def disutility(demand_i, node_i, gamma_i, pi_g, e_g, node_j, k_j, pi_j, e_j):
    demand_j = cp.Variable(k_j, nonneg=True)
    r_ij = Resistance(node_i, node_j) * 1000
    v = 240
    disutility = demand_j[0] * (pi_j[0] + gamma_i * e_j[0] - pi_g - gamma_i * e_g) + \
                  demand_j[1] * (pi_j[1] + gamma_i * e_j[1] - pi_g - gamma_i * e_g)\
                  + (demand_j[0] + demand_j[1])**2 * (pi_g + gamma_i * e_g) * r_ij/v**2
    objective = cp.Minimize(disutility)
    constraint = demand_i - cp.sum(demand_j)
    constraints = [constraint >= 0]
    prob = cp.Problem(objective, constraints)
    utility = -1 * prob.solve(solver=cp.GUROBI, reoptimize=True)
    demand = demand_j.value
    bid_ij = [utility, demand[0], demand[1]]
    return bid_ij



#bid = disutility(5, 9, 0.1, 0.20, 0.3, 35, 2, [10, 10], [0.1, 0.1])
#print(bid)

print(f'time: {time() - start} seconds')

#print(cp.installed_solvers())
