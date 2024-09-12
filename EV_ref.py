import pandas as pd
import numpy as np
import cvxpy as cp
from time import time
start = time()

###  initialisation  ###
consumption = pd.read_csv('./data/consumption_data.csv')
der = pd.read_csv('./data/der.csv')
EV = pd.read_csv('./data/EV.csv')

l = EV['vehicle']
ta = EV['ta']
td = EV['td']
SOC_a = EV['soc_a']
SOC_d = EV['soc_d']
SOC_min = EV['soc_min']
SOC_max = EV['soc_max']
Pl_max = EV['p_max']
capacity = EV['capacity']
eta_c = EV['eta_c']
eta_d = EV['eta_d']

####  grid  ####

grid_price = consumption['price_grid']
grid_emf = consumption['emf_grid']

PV_gen = consumption['pv_charging']

#####  parameters  #####

price_RE = 1.05
price_EV = 1.00
eta_inv = 0.98

#### scheduling instances ####

for i in range(len(l)):
    scheduling_horizon = td[i] - ta[i]
    charging_grid = cp.Variable(scheduling_horizon, nonneg=True)

    def soc(i, t_s, t_f):
        SOC_init = SOC_a[i]
        SOC = SOC_init
        for tau in range(t_s, t_f):
            SOC += (charging_grid[tau] * eta_c[i]) / capacity[i]
        return SOC


    constraints = []
    constraints += [soc(i, 0, td[i] - ta[i]) == SOC_d[i]]

    for t in range(ta[i], td[i]):
        constraints += [charging_grid[t-ta[i]] <= Pl_max[i]]

    cost = 0
    for t in range(ta[i], td[i]):
        cost += charging_grid[t-ta[i]] * grid_price[t]

    objective = cp.Minimize(cost)
    prob = cp.Problem(objective, constraints)
    print(prob.solve(solver=cp.GUROBI, reoptimize=True, verbose=True))

    charging_grid_actual = charging_grid.value

    def soc_actual(i, t_s, t_f):
        SOC_init = SOC_a[i]
        SOC = SOC_init
        for tau in range(t_s, t_f):
            SOC += (charging_grid_actual[tau] * eta_c[i]) / capacity[i]
        return SOC

    results = pd.read_csv('./data/EV_ref_results.csv')

    charging_grid_label = 'charging_grid_' + str(i)
    soc_label = 'soc_' + str(i)

    for ts in range(ta[i], td[i]):
        results.at[ts, charging_grid_label] = charging_grid_actual[ts-ta[i]]
        results.at[ts, soc_label] = soc_actual(i, 0, ts-ta[i])

    #loc = './data/EV_results' + str(t) + '.csv'
    loc = './data/EV_ref_results.csv'
    df = pd.DataFrame.from_dict(results)
    df.to_csv(loc, index=False, header=True)

results = pd.read_csv('./data/EV_ref_results.csv')



print(f'time: {time() - start} seconds')







#print(prob.solve(solver=cp.CVXOPT, max_iters=10000, reltol=1e-6, abstol=1e-6, feastol=1e-6, verbose=False))
#print(action.value)

# results = {'charging_RE': charging_RE.value, 'charging_grid': charging_grid.value, 'discharging': discharging.value,
#            'RE_cap': RE_cap, 'price': grid_price}
#
# df = pd.DataFrame.from_dict(results)
# df.to_csv('./data/battery.csv', index = False, header=True)
# print(f'time: {time() - start} seconds')

#print(cp.installed_solvers())
