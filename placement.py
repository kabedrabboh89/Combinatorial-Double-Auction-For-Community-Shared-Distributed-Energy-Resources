import pandas as pd
import numpy as np
from utility import disutility
from time import time
import os
start = time()


####  initialisation  ####



for i in range(1, 38):
    if i == 8:
        continue
    if i == 14:
        continue
    if i == 7:
        continue
    if i == 9:
        continue
    if i == 12:
        continue
    placement = pd.read_csv('./placement.csv')
    ders = pd.read_csv('./data/der.csv')
    ders.at[1, 'node'] = i
    df = pd.DataFrame(ders)
    df.to_csv('./data/der.csv', index=False)
    os.system('python main.py')
    print('main')
    os.system('python SWO.py')
    print('SWO')
    # os.system('python post_processing.py')
    # print('post')
    post = pd.read_csv('./post.csv')
    vtotal_100_losses = post['total_100_losses']
    vtotal_100_der = post['total_100_der']
    vtotal_100 = post['total_100']
    vemf_grid = post['emf_grid']
    vtotal_100_grid = post['total_100_grid']
    vtotal_100_ei = post['total_100_ei']
    vrevenue_der1 = post['revenue_der1']
    vrevenue_der2 = post['revenue_der2']
    vrevenue_der3 = post['revenue_der3']
    vder11 = post['der11']
    vder12 = post['der12']
    vder21 = post['der21']
    vder22 = post['der22']
    vder31 = post['der31']
    vder32 = post['der32']
    total_100_losses = 0
    total_100_der = 0
    total_100 = 0
    emf_grid = 0
    total_100_grid = 0
    total_100_ei = 0
    revenue_der1 = 0
    revenue_der2 = 0
    revenue_der3 = 0
    der11 = 0
    der12 = 0
    der21 = 0
    der22 = 0
    der31 = 0
    der32 = 0
    for t in range(24):
        total_100_losses += vtotal_100_losses[t]
        total_100_der += vtotal_100_der[t]
        total_100 += vtotal_100[t]
        emf_grid += vemf_grid[t]
        total_100_grid += vtotal_100_grid[t]
        total_100_ei += vtotal_100_ei[t]
        revenue_der1 += vrevenue_der1[t]
        revenue_der2 += vrevenue_der2[t]
        revenue_der3 += vrevenue_der3[t]
        der11 += vder11[t]
        der12 += vder12[t]
        der21 += vder21[t]
        der22 += vder22[t]
        der31 += vder31[t]
        der32 += vder32[t]

    placement.at[i-1, 'total_100_losses'] = total_100_losses
    placement.at[i-1, 'total_100_der'] = total_100_der
    placement.at[i-1, 'total_100'] = total_100
    placement.at[i-1, 'emf_grid'] = emf_grid
    placement.at[i-1, 'total_100_grid'] = total_100_grid
    placement.at[i-1, 'total_100_ei'] = total_100_ei
    placement.at[i-1, 'revenue_der1'] = revenue_der1
    placement.at[i-1, 'revenue_der2'] = revenue_der2
    placement.at[i-1, 'revenue_der3'] = revenue_der3
    placement.at[i-1, 'der11'] = der11
    placement.at[i-1, 'der12'] = der12
    placement.at[i-1, 'der21'] = der21
    placement.at[i-1, 'der22'] = der22
    placement.at[i-1, 'der31'] = der31
    placement.at[i-1, 'der32'] = der32
    print(i)
    print(f'time: {time() - start} seconds')
    df = pd.DataFrame(placement)
    df.to_csv('./placement.csv', index=False)




####  DERs  ####





print(f'time: {time() - start} seconds')

