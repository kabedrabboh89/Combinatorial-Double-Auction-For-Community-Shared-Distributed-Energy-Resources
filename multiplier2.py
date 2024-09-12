import pandas as pd
import numpy as np
from utility import disutility
from time import time
import importlib
import os
start = time()

price_multiplier = ["1", "1.1", "1.2", "1.3", "1.4"]
gamma_multiplier = ["0.05", "0.1", "0.15", "0.2", "0.25"]

revenue_df = pd.read_csv('./DER2/revenue.csv')
charging_re_df = pd.read_csv('./DER2/charging_re.csv')

for i in price_multiplier:
    path = './DER2/der' + i + '.csv'
    der1 = pd.read_csv(path)
    df = pd.DataFrame(der1)
    df.to_csv('./data/der.csv', index=False)
    l = 0
    for j in gamma_multiplier:
        path = './DER2/consumers' + j + '.csv'
        consumers = pd.read_csv(path)
        df1 = pd.DataFrame(consumers)
        df1.to_csv('./data/consumers.csv', index=False)
        os.system('python main.py')
        os.system('python SWO.py')
        os.system('python post_DER2.py')
        post = pd.read_csv('./post_DER2_results.csv')
        revenueij = post['revenue_der2']
        re_charging_ij = post['charging_RE']
        revenue = 0
        re_charging = 0
        for k in range(24):
            revenue += revenueij[k]
            re_charging += re_charging_ij[k]
        revenue_df.at[l, str(j)] = revenue
        charging_re_df.at[l, str(j)] = re_charging
        df2 = pd.DataFrame(post)
        df2.to_csv('./DER2/post' + i + 'x' + j + '.csv', index=False)
    l += 1


df3 = pd.DataFrame(revenue_df)
df3.to_csv('./DER2/revenue.csv', index=False)
df4 = pd.DataFrame(charging_re_df)
df4.to_csv('./DER2/charging_re.csv', index=False)



        # path = './DER1/DER1_results_' + i + 'x' + j + '.csv'
        # der1 = pd.read_csv(path)
        # ders = pd.read_csv('./DER1/der.csv')
        # ders['s1_der1_cap'] = der1['RE_cap']
        # ders['s1_der1_pi'] = der1['RE_price']
        # ders['s1_der1_emf'] = der1['emf_re']
        # ders['s1_der2_cap'] = der1['discharging']
        # ders['s1_der2_pi'] = der1['BESS_price']
        # ders['s1_der2_emf'] = der1['emf_bess']
        # ders['charging_RE'] = der1['charging_RE']
        # ders['charging_grid'] = der1['charging_grid']
        # df = pd.DataFrame(ders)


# print(f'time: {time() - start} seconds')
#
# importlib.import_module('SWO')
# importlib.import_module('post_processing')
#
#
# print(f'time: {time() - start} seconds')

