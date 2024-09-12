import pandas as pd
import cvxpy as cp
import numpy as np
from time import time
start = time()

###  initialisation  ###
consumption = pd.read_csv('./data/consumption_data.csv')
der = pd.read_csv('./data/der.csv')
EV = pd.read_csv('./data/EV_t2.csv')

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

RE_cap = der['s1_der1_cap']

t = min(ta)

scheduling_horizon = max(td) - t

print(t, scheduling_horizon)

charging_RE = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
charging_grid = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
discharging = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)


def soc(i, t_start, t_soc):
    SOC = SOC_a[i]
    for tau in range(t_start, t_soc):
        SOC += (charging_grid[i][tau] * eta_c[i] + charging_RE[i][tau] * eta_c[i] -
                discharging[i][tau] / eta_d[i]) / capacity[i]
    return SOC

constraints = []

for i in range(len(l)):
    constraints += [soc(i, ta[i]-t, td[i]-t) == SOC_d[i]]
    for ts in range(t, t + scheduling_horizon):
        if ts not in range(ta[i], td[i]):
            constraints += [charging_grid[i][ts-t] == 0, charging_RE[i][ts-t] == 0, discharging[i][ts-t] == 0]
        else:
            constraints += [(charging_grid[i][ts-t]+charging_RE[i][ts-t])/capacity[i] <= Pl_max[i],
                            discharging[i][ts-t]/capacity[i] <= Pl_max[i]]
            constraints += [soc(i, 0, ts-t+1) >= SOC_min[i], soc(i, 0, ts-t+1) <= SOC_max[i]]


for ts in range(t, t + scheduling_horizon):
    constraints += [cp.sum(charging_RE, axis=0)[ts-t] <= RE_cap[ts]]


cost = 0
for ts in range(t, t + scheduling_horizon):
    cost += cp.sum(charging_grid, axis=0)[ts-t] * grid_price[ts]


revenue = 0
for ts in range(t, t + scheduling_horizon):
    revenue += (RE_cap[ts]-cp.sum(charging_RE, axis=0)[ts-t]) * grid_price[ts] + \
               cp.sum(discharging, axis=0)[ts-t] * grid_price[ts]


objective = cp.Maximize(revenue-cost)
prob = cp.Problem(objective, constraints)
print(prob.solve(verbose=True))

charging_RE_results = charging_RE.value
df = pd.DataFrame.from_dict(charging_RE_results)
df.to_csv('./EV/charging_RE_results.csv')

discharging_results = discharging.value
df = pd.DataFrame.from_dict(discharging_results)
df.to_csv('./EV/discharging_results.csv')

charging_grid_results = charging_grid.value
df = pd.DataFrame.from_dict(charging_grid_results)
df.to_csv('./EV/charging_grid_results.csv')



####  optimization  ####

# charging_RE = cp.Variable(shape=(l, 24), nonneg=True)
# charging_grid = cp.Variable(shape=(l, 24), nonneg=True)
# discharging = cp.Variable(shape=(l, 24), nonneg=True)
#
#

#
#
# constraints = []
#
# for i in range(l):
#     constraints += [soc(i, td[i]) == SOC_d[i]]
#     for t in range(24):
#         if t not in range(ta[i], td[i]):
#             constraints += [charging_grid[i][t] == 0, charging_RE[i][t] == 0, discharging[i][t] == 0]
#         else:
#             constraints += [(charging_grid[i][t]+charging_RE[i][t])/capacity[i] <= Pl_max[i],
#                             discharging[i][t]/capacity[i] <= Pl_max[i]]
#             #constraints += [soc(i, t) >= SOC_min[i], soc(i, t) <= SOC_max[i]]
#
#
# for t in range(24):
#     constraints += [cp.sum(charging_RE, axis=1)[t] <= RE_cap[t]]
#
#
# cost = 0
# for t in range(24):
#     for i in range(l):
#         cost += charging_grid[i][t] * grid_price[t]
#
#
# revenue = 0
# for t in range(24):
#     revenue += (RE_cap[t]-cp.sum(charging_RE, axis=1)[t]) * grid_price[t] + \
#                cp.sum(discharging, axis=1)[t] * grid_price[t]
#
#
# objective = cp.Maximize(revenue-cost)
# prob = cp.Problem(objective, constraints)
# print(prob.solve(verbose=True))
# #print(prob.solve(solver=cp.CVXOPT, max_iters=10000, reltol=1e-6, abstol=1e-6, feastol=1e-6, verbose=False))
# #print(action.value)
#
# # results = {'charging_RE': charging_RE.value, 'charging_grid': charging_grid.value, 'discharging': discharging.value,
# #            'RE_cap': RE_cap, 'price': grid_price}
# #
# # df = pd.DataFrame.from_dict(results)
# # df.to_csv('./data/battery.csv', index = False, header=True)
# # print(f'time: {time() - start} seconds')
#
# #print(cp.installed_solvers())
