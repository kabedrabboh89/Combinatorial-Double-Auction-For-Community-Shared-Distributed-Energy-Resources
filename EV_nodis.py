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

####  grid  ####

grid_price = consumption['price_grid']
grid_emf = consumption['emf_grid']

PV_gen = consumption['pv_charging']

#####  parameters  #####

price_RE = 1.05
price_EV = 1.00
eta_inv = 0.98

#### scheduling instances ####
ts_all =[]
ta_dummy = np.zeros(len(l))
for i in range(len(l)):
    ta_dummy[i] = ta[i]
for t in range(24):
    if t not in ta_dummy:
        continue
    else:
        ts_all.append(t)

EV_df = pd.DataFrame(EV, index=range(len(l)))

for t in ts_all:
    EV_df1 = EV_df
    for i in range(len(l)):
        if t not in range(ta[i], td[i]):
            EV_df1 = EV_df1.drop(index=i)
    EV_df1.reset_index(inplace=True)
    df = pd.DataFrame.from_dict(EV_df1)
    location = './data/EV_t' + str(t) + '.csv'
    df.to_csv(location, index=False, header=True)


####  optimization  ####
counter = 0

for t in ts_all:
    counter += 1
    ts_dummy = ts_all
    data = './data/EV_t' + str(t) + '.csv'
    EV = pd.read_csv(data)
    index = EV['index']
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

    tf = max(td)
    scheduling_horizon = tf - t

    charging_RE = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
    charging_grid = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)
    #discharging = cp.Variable(shape=(len(l), scheduling_horizon), nonneg=True)


    def soc(i, t_s, t_f):
        SOC_init = SOC_a[i]
        SOC = SOC_init
        for tau in range(t_s, t_f):
            SOC += (charging_grid[i][tau] * eta_c[i] + charging_RE[i][tau] * eta_c[i]) / capacity[i]
        return SOC


    constraints = []
    for i in range(len(l)):
        constraints += [soc(i, 0, td[i]-t) == SOC_d[i]]
        for ts in range(t, t + scheduling_horizon):
            if ts not in range(ta[i], td[i]):
                constraints += [charging_grid[i][ts-t] == 0, charging_RE[i][ts-t] == 0]
            else:
                constraints += [(charging_grid[i][ts-t]+charging_RE[i][ts-t]) <= Pl_max[i]]
                constraints += [soc(i, 0, ts-t+1) >= SOC_min[i], soc(i, 0, ts-t+1) <= SOC_max[i]]


    for ts in range(t, t + scheduling_horizon):
        constraints += [cp.sum(charging_RE, axis=0)[ts-t]/eta_inv <= PV_gen[ts]]


    cost = 0
    for ts in range(t, t + scheduling_horizon):
        cost += cp.sum(charging_grid, axis=0)[ts-t] * grid_price[ts]


    objective = cp.Minimize(cost)
    prob = cp.Problem(objective, constraints)
    print(prob.solve(solver=cp.GUROBI, reoptimize=True, verbose=True))

    charging_grid_actual = charging_grid.value
    charging_RE_actual = charging_RE.value
    #discharging_actual = discharging.value

    def soc_actual(i, t_s, t_f):
        SOC_init = SOC_a[i]
        SOC = SOC_init
        for tau in range(t_s, t_f):
            SOC += (charging_grid_actual[i][tau] * eta_c[i] + charging_RE_actual[i][tau] * eta_c[i]) / capacity[i]
        return SOC

    results = pd.read_csv('./data/EV_ref_results.csv')

    for i in range(len(l)):
        charging_grid_label = 'charging_grid_' + str(index[i])
        charging_re_label = 'charging_re_' + str(index[i])
        #discharging_label = 'discharging_' + str(index[i])
        soc_label = 'soc_' + str(index[i])
        for ts in range(t, t + scheduling_horizon):
            results.at[ts, charging_grid_label] = charging_grid_actual[i][ts-t]
            results.at[ts, charging_re_label] = charging_RE_actual[i][ts - t]
            #results.at[ts, discharging_label] = discharging_actual[i][ts - t]
            results.at[ts, soc_label] = soc_actual(i, t-t, ts-t)

    #loc = './data/EV_results' + str(t) + '.csv'
    loc = './data/EV_ref_results.csv'
    df = pd.DataFrame.from_dict(results)
    df.to_csv(loc, index=False, header=True)

    print(t)
    print(f'time: {time() - start} seconds')

    if counter >= len(ts_all):
        break

    next_time = ts_all[counter]
    target_df_loc = './data/EV_t' + str(next_time) + '.csv'
    next_data = pd.read_csv(target_df_loc)
    index_next = next_data['index']

    for j in range(len(index_next)):
        for i in range(len(l)):
            soc_next_time = soc_actual(i, t-t, next_time-t)
            if index[i] == index_next[j]:
                next_data.at[j, 'soc_a'] = soc_next_time

    df = pd.DataFrame.from_dict(next_data)
    df.to_csv(target_df_loc, index=False, header=True)

results = pd.read_csv('./data/EV_ref_results.csv')
charging_grid_total = np.zeros(24)
charging_RE_total = np.zeros(24)
discharging_total = np.zeros(24)

for t in range(24):
    for i in range(25):
        charging_grid_label = 'charging_grid_' + str(i)
        charging_re_label = 'charging_re_' + str(i)
        discharging_label = 'discharging_' + str(i)
        charging_grid = results[charging_grid_label]
        charging_RE = results[charging_re_label]
        discharging = results[discharging_label]
        charging_grid_total[t] += charging_grid[t]
        charging_RE_total[t] += charging_RE[t]
        discharging_total[t] += discharging[t]

df = pd.DataFrame.from_dict(results)
df['charging_grid_total'] = charging_grid_total
df['charging_RE_total'] = charging_RE_total
df['discharging_total'] = discharging_total


loc = './data/EV_ref_results.csv'

df.to_csv(loc, index=False, header=True)

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
