import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='13')
# --- FORMAT 1

DER1_BESS = pd.read_csv('./data/basic results/DER1_results.csv')
DER2_BESS = pd.read_csv('./data/basic results/DER2_results.csv')

soc1 = DER1_BESS['soc']
soc2 = DER2_BESS['soc']

df = pd.read_csv('./data/basic results/basic_results.csv')

# --- FORMAT 2</pre>
hour = df['hour']
grid_demand = df['grid_demand']
grid_demand_CDA = df['grid_demand_CDA']

EV_demand = df['EV_demand']
EV_demand_CDA = df['EV_demand_CDA']

der1 = df['pv_rooftop']
der2 = df['wind']
der3 = df['pv_charging']

der11 = df['der11']
der12 = df['der12']
der21 = df['der21']
der22 = df['der22']
der31 = df['der31']
der32 = df['der32']

offered_der11 = df['offered_der11']
offered_der12 = df['offered_der12']
offered_der21 = df['offered_der21']
offered_der22 = df['offered_der22']
offered_der31 = df['offered_der31']
offered_der32 = df['offered_der32']

cum_cost = df['cum_cost']
cum_cost_CDA = df['cum_cost_CDA']

cum_EI = df['cum_EI']
cum_EI_CDA = df['cum_EI_CDA']

cum_revenue1 = df['cum_revenue1']
cum_revenue1_CDA = df['cum_revenue1_CDA']

cum_revenue2 = df['cum_revenue2']
cum_revenue2_CDA = df['cum_revenue2_CDA']

cum_revenue3 = df['cum_revenue3']
cum_revenue3_CDA = df['cum_revenue3_CDA']

################
consumption = pd.read_csv('./data/consumption_data_demand.csv')
consumers = pd.read_csv('./data/consumers.csv')

consumer = consumers['consumer']
nodes_i = consumers['node']


demand = pd.read_csv('./demand.csv')

nodes = [2, 5, 7, 9,10,12,14,15,16,18,20,21,24,27,28,32,33,34,36,37]

current_node = 2
consumers_node = []

for i in range(100):
    if nodes_i[i] == current_node:
        consumers_node += [i+1]

consumption_node = np.zeros(24)
demand_der_node = np.zeros(24)
demand_grid_node = np.zeros(24)
losses_node = np.zeros(24)

for t in range(24):
    for l in consumers_node:
        print(str(l))
        consumption_identifier = 'D'+ str(l)
        demand_der_identifier = 'der' + str(l)
        demand_grid_identifier = str(l)
        losses_identifier = 'losses' + str(l)
        consumption_node[t] += consumption[consumption_identifier][t]
        demand_der_node[t] += demand[demand_der_identifier][t]
        demand_grid_node[t] += demand[demand_grid_identifier][t]
        losses_node[t] += demand[losses_identifier][t]


# --- FORMAT 2</pre>
hour = consumption['hour']


fig, (ax1, ax2) = plt.subplots\
    (ncols=2, subplot_kw=dict(frameon=False), figsize=(14, 5))

plt.subplots_adjust(wspace=0.3, left=0.12, right=0.98, top=0.98, bottom=0.22)


ax1.set_ylabel('DER\n Type I\n BESS\n utilisation\n(%)', fontproperties='Arial', size='16', rotation=0)
ax2.set_ylabel('DER\n Type II\n BESS\n utilisation\n(%)', fontproperties='Arial', size='16', rotation=0)
ax1.set_xlabel('time (hour)\n\n(a)', fontproperties='Arial', size='16',
               rotation=0)
ax2.set_xlabel('time (hour)\n\n(b)', fontproperties='Arial', size='16',
               rotation=0)

ax6 = ax1.twinx()
ax7 = ax2.twinx()

ax1.yaxis.set_label_coords(-0.18,0.4)
ax2.yaxis.set_label_coords(-0.18,0.4)


ax1.set_xlim([0, 25])
ax1.set_xticks(hour)
ax1.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])

ax2.set_xlim([0, 25])
ax2.set_xticks(hour)
ax2.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])

ax1.set_ylim([0, 110])
ax1.set_yticks([20, 90])
ax1.set_yticklabels([r'$SoC_i$  '+'\n(20%)', r'$SoC_{max}$'+'\n(90%)  '])

ax2.set_ylim([0, 110])
ax2.set_yticks([20, 90])
ax2.set_yticklabels([r'$SoC_i$  '+'\n(20%)', r'$SoC_{max}$'+'\n(90%)  '])

ax6.set_yticks([])
ax6.set_yticklabels([])
ax7.set_yticks([])
ax7.set_yticklabels([])

ax1.bar(hour, soc1, color='green', label='Offered RE')
#ax1.plot(hour, der11, color='green', label='RE supply', drawstyle='steps-post')
ax2.bar(hour, soc2, color='green', label='Offered BESS')
ax2.plot(hour, der12, color='green', label='BESS supply', drawstyle='steps-post')
#ax2.bar(hour, EV_demand_CDA, color='green', label='grid demand')
# ax2.bar(hour, demand_der_node, color='green', bottom=demand_grid_node, label='DER demand')
# ax2.bar(hour, losses_node, color='darkred', bottom=demand_der_node + demand_grid_node, label='losses')

# ax1.legend(loc='upper left', fontsize='16')
# ax2.legend(loc='upper left', fontsize='16')

plt.savefig('./BESS_utilisation.png', dpi=600)
plt.show()