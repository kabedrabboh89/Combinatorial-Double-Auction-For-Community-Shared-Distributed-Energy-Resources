import pandas as pd
import numpy as np
from utility import disutility
from time import time
import importlib
import os
start = time()

PV_multiplier = ["10"]
BESS_multiplier = ["5"]

revenue_df = pd.read_csv('./DER1/revenue.csv')
charging_re_df = pd.read_csv('./DER1/charging_re.csv')

l=7
for i in PV_multiplier:
    for j in BESS_multiplier:
        path = './DER1/der' + i + 'x' + j + '.csv'
        der1 = pd.read_csv(path)
        df = pd.DataFrame(der1)
        df.to_csv('./data/der.csv', index=False)
        os.system('python main.py')
        os.system('python SWO.py')
        os.system('python post_DER1.py')
        post = pd.read_csv('./post_DER1.csv')
        revenueij = post['revenue_der1']
        re_charging_ij = post['charging_RE']
        revenue = 0
        re_charging = 0
        for k in range(24):
            revenue += revenueij[k]
            re_charging += re_charging_ij[k]
        revenue_df.at[l, str(j)] = revenue
        charging_re_df.at[l, str(j)] = re_charging
        df1 = pd.DataFrame(post)
        df1.to_csv('./DER1/post' + i + 'x' + j + '.csv', index=False)
    l += 1


df2 = pd.DataFrame(revenue_df)
df2.to_csv('./DER1/revenue.csv', index=False)
df3 = pd.DataFrame(charging_re_df)
df3.to_csv('./DER1/charging_re.csv', index=False)



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

