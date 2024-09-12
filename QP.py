import numpy as np
import pandas as pd
import cvxpy as cp
from time import time
start = time()

###  initialisation  ###
consumption = pd.read_csv('./data/consumption_data.csv')
der = pd.read_csv('./data/der.csv')


####  grid  ####

grid_price = consumption['price_grid']
grid_emf = consumption['emf_grid']

RE_cap = der['s1_der1_cap']

battery_cap = 27
power = 10
eta_c = 0.97468
eta_d = 0.97468

charging_RE = cp.Variable(24, nonneg=True)
charging_grid = cp.Variable(24, nonneg=True)
discharging = cp.Variable(24, nonneg=True)

charging = charging_RE + charging_grid
constraints = [discharging <= power, charging <= power]

cost = 0
for i in range(24):
    cost += charging_grid[i] * grid_price[i]


revenue = 0
for i in range(24):
    revenue += (RE_cap[i]-charging_RE[i]) * 0.5 * grid_price[i] + discharging[i] * grid_price[i]

def soc(i):
    soc = 0
    for t in range(i+1):
        soc += charging[t] * eta_c - discharging[t]/eta_d
    return soc

for i in range(24):
    constraints += [soc(i) >=0, soc(i) <= battery_cap]
    constraints += [charging_RE <= RE_cap]


objective = cp.Maximize(revenue-cost)
prob = cp.Problem(objective, constraints)
print(prob.solve(verbose=True))
#print(prob.solve(solver=cp.CVXOPT, max_iters=10000, reltol=1e-6, abstol=1e-6, feastol=1e-6, verbose=False))
#print(action.value)

results = {'charging_RE': charging_RE.value, 'charging_grid': charging_grid.value, 'discharging': discharging.value,
           'RE_cap': RE_cap, 'price': grid_price}

df = pd.DataFrame.from_dict(results)
df.to_csv('./data/battery.csv', index = False, header=True)
print(f'time: {time() - start} seconds')

#print(cp.installed_solvers())
