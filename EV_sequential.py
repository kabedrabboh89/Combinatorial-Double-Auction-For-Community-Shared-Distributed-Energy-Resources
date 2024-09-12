import pandas as pd
import cvxpy as cp
import numpy as np
from time import time
start = time()

charging_grid_actual = np.zeros((len(l), scheduling_horizon))
    charging_RE_actual = np.zeros((len(l), scheduling_horizon))
    discharging_actual = np.zeros((len(l), scheduling_horizon))
    for n in range(len(l)):
        for m in range(scheduling_horizon):
            charging_grid_actual[n][m] = charging_grid[n][m].value
            charging_RE_actual[n][m] = charging_RE[n][m].value
            discharging_actual[n][m] = discharging[n][m].value
###  initialisation  ###
consumption = pd.read_csv('./data/consumption_data.csv')
der = pd.read_csv('./data/der.csv')
EV = pd.read_csv('./data/EV.csv')

l = EV['vehicle']
ta = EV['ta']
td = EV['td']
# SOC_a = EV['soc_a']
# SOC_d = EV['soc_d']
# SOC_min = EV['soc_min']
# SOC_max = EV['soc_max']
# Pl_max = EV['p_max']
# capacity = EV['capacity']
# eta_c = EV['eta_c']
# eta_d = EV['eta_d']
#
# ####  grid  ####
#
# grid_price = consumption['price_grid']
# grid_emf = consumption['emf_grid']
#
# RE_cap = der['s1_der1_cap']
#
#
# EV_dict = {'vehicle': l, 'ta': ta, 'td': td, 'SOC_i': SOC_a, 'SOC_d': SOC_d, 'SOC_min': SOC_min, 'SOC_max': SOC_max,
#            'P_max': Pl_max, 'capacity': capacity, 'eta_c': eta_c, 'eta_d': eta_d}
EV_df = pd.DataFrame(EV, index=range(len(l)))

#updating_counter = -1

for t in range(24):
    print(t)
    l = EV_df['vehicle']
    ta = EV_df['ta']
    td = EV_df['td']
    EV_df1 = EV_df
    ta_dummy = np.zeros(len(l))
    for i in range(len(l)):
        ta_dummy[i] = ta[i]
    if t not in ta_dummy:
        continue
    for i in range(len(l)):
        if t not in range(ta[i], td[i]):
            EV_df1 = EV_df1.drop(index=i)
    EV_df1.reset_index(inplace=True)
    df = pd.DataFrame.from_dict(EV_df1)
    location = './data/EV_t' + str(t) + '.csv'
    df.to_csv(location, index=False, header=True)
    #
    # l = EV_df1['vehicle']
    # ta = EV_df1['ta']
    # td = EV_df1['td']
    # SOC_a = EV_df1['SOC_i']
    # SOC_d = EV_df1['SOC_d']
    # SOC_min = EV_df1['SOC_min']
    # SOC_max = EV_df1['SOC_max']
    # Pl_max = EV_df1['P_max']
    # capacity = EV_df1['capacity']
    # eta_c = EV_df1['eta_c']
    # eta_d = EV_df1['eta_d']
    # index = EV_df1['index']
    #
    # if len(l)<1:
    #     continue
    #
    # def update_soc(t):
    #     for i in range(len(l)):
    #         soc_t = SOC_a[i] + (charging_grid[i][t].value * eta_c[i] + charging_RE[i][t].value * eta_c[i] -
    #                   discharging[i][t].value / eta_d[i]) / capacity[i]
    #         dummy_var = index[i]
    #         EV_df.at[dummy_var, 'SOC_i'] = soc_t
    #
    # ta_dummy = np.zeros(len(l))
    # for i in range(len(l)):
    #     ta_dummy[i] = ta[i]
    # if t not in ta_dummy:
    #     updating_counter += 1
    #     update_soc(updating_counter)
    #     continue
    # else:
    #     updating_counter = -1
    #
    # scheduling_horizon = max(td) - t
    #
    # charging_RE = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
    # charging_grid = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
    # discharging = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
    #
    #
    # def soc(i, t_start, t_soc):
    #     SOC = SOC_a[i]
    #     for tau in range(t_start, t_soc):
    #         SOC += (charging_grid[i][tau] * eta_c[i] + charging_RE[i][tau] * eta_c[i] -
    #                 discharging[i][tau] / eta_d[i]) / capacity[i]
    #     return SOC
    #
    # constraints = []
    #
    # for i in range(len(l)):
    #     constraints += [soc(i, ta[i]-t, td[i]-t) == SOC_d[i]]
    #     for ts in range(t, t + scheduling_horizon):
    #         if ts not in range(ta[i], td[i]):
    #             constraints += [charging_grid[i][ts-t] == 0, charging_RE[i][ts-t] == 0, discharging[i][ts-t] == 0]
    #         else:
    #             constraints += [(charging_grid[i][ts-t]+charging_RE[i][ts-t])/capacity[i] <= Pl_max[i],
    #                             discharging[i][ts-t]/capacity[i] <= Pl_max[i]]
    #             constraints += [soc(i, 0, ts-t+1) >= SOC_min[i], soc(i, 0, ts-t+1) <= SOC_max[i]]
    #
    #
    # for ts in range(t, t + scheduling_horizon):
    #     constraints += [cp.sum(charging_RE, axis=0)[ts-t] <= RE_cap[ts]]
    #
    #
    # cost = 0
    # for ts in range(t, t + scheduling_horizon):
    #     cost += cp.sum(charging_grid, axis=0)[ts-t] * grid_price[ts]
    #
    #
    # revenue = 0
    # for ts in range(t, t + scheduling_horizon):
    #     revenue += (RE_cap[ts]-cp.sum(charging_RE, axis=0)[ts-t]) * grid_price[ts] + \
    #                cp.sum(discharging, axis=0)[ts-t] * grid_price[ts]
    #
    #
    # objective = cp.Maximize(revenue-cost)
    # prob = cp.Problem(objective, constraints)
    # print(prob.solve(verbose=True))
    #
    # update_soc(1)
    #
    #
    #

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
