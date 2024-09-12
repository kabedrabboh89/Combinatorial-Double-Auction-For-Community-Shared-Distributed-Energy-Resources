import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='13')
# --- FORMAT 1

df = pd.read_csv('./main_results.csv')

# --- FORMAT 2</pre>
hour = df['hour']
grid_demand_case1 = df['grid_demand_case1']
grid_demand_case2 = df['grid_demand_case2']
grid_demand_CDA = df['grid_demand_CDA']

EV_demand_case1 = df['EV_demand_case1']
EV_demand_case2 = df['EV_demand_case2']
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

der11_case2 = df['1']
der12_case2 = df['2']
der21_case2 = df['3']
der22_case2 = df['4']
der31_case2 = df['5']
der32_case2 = df['6']

offered_der11 = df['offered_der11']
offered_der12 = df['offered_der12']
offered_der21 = df['offered_der21']
offered_der22 = df['offered_der22']
offered_der31 = df['offered_der31']
offered_der32 = df['offered_der32']

cum_cost_case1 = df['cum_cost_case1']
cum_cost_case2 = df['cum_cost_case2']
cum_cost_CDA = df['cum_cost_CDA']

cum_EI_case1 = df['cum_EI_case1']
cum_EI_case2 = df['cum_EI_case2']
cum_EI_CDA = df['cum_EI_CDA']

cum_revenue1_case1 = df['cum_revenue1_case1']
cum_revenue1_case2 = df['cum_revenue1_case2']
cum_revenue1_CDA = df['cum_revenue1_CDA']

cum_revenue2_case1 = df['cum_revenue2_case1']
cum_revenue2_case2 = df['cum_revenue2_case2']
cum_revenue2_CDA = df['cum_revenue2_CDA']

cum_revenue3_case1 = df['cum_revenue3_case1']
cum_revenue3_case2 = df['cum_revenue3_case2']
cum_revenue3_CDA = df['cum_revenue3_CDA']

cum_losses_wo = df['cum_losses_wo']
cum_losses_opt = df['cum_losses_opt']


fig, ax1 = plt.subplots\
    (subplot_kw=dict(frameon=False), figsize=(7, 4))

plt.subplots_adjust(hspace=.0, left=0.225, right=0.98, top=1, bottom=0.15)



ax1.set_ylabel('grid\n demand\n (kWh)', fontproperties='Arial', size='16', rotation=0)
#ax2.set_ylabel('EV\n demand\n (kWh)', fontproperties='Arial', size='16', rotation=0)
#ax3.set_ylabel('DER\n Type I\n supply\n (kWh)', fontproperties='Arial', size='16', rotation=0)
#ax4.set_ylabel('DER\n Type II\n supply\n (kWh)', fontproperties='Arial', size='16', rotation=0)
#ax5.set_ylabel('DER\n Type III\n supply\n (kWh)', fontproperties='Arial', size='16', rotation=0)

ax1.set_xlabel('time (hour)', fontproperties='Arial', size='16',
               rotation=0)
# ax4.set_ylabel('cumulative\n cost\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
# ax5.set_ylabel('cumulative\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
ax6 = ax1.twinx()
#ax7 = ax2.twinx()
#ax8 = ax3.twinx()
#ax9 = ax4.twinx()
#ax10 = ax5.twinx()
#ax9.set_ylabel('cumulative\n emissions\n (kg.CO'+r'$_2$)', fontproperties='Arial', size='11', rotation=0)

ax1.yaxis.set_label_coords(-0.18,0.4)
#ax2.yaxis.set_label_coords(-0.18,0.4)
#ax3.yaxis.set_label_coords(-0.18,0.4)
#ax4.yaxis.set_label_coords(-0.18,0.4)
#ax5.yaxis.set_label_coords(-0.18,0.4)
# ax9.yaxis.set_label_coords(1.1,1)

ax1.set_xlim([0, 25])
#plt.xticks(hour, hour, fontproperties='Arial', size = '16')
ax1.set_xticks(hour)
ax1.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])
#ax1.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
#                     "16", "17", "18", "19", "20", "21", "22", "23", "24"])


ax1.set_ylim([50, 350])
#ax2.set_ylim([0, 240])
#ax3.set_ylim([0, 65])
#ax4.set_ylim([0, 90])
#ax5.set_ylim([0, 85])
# ax4.set_ylim([0, 1200])
# ax5.set_ylim([0, 190])
# ax9.set_ylim([0, 2700000])

ax1.set_yticks(np.linspace(100, 250, 4))
ax1.set_yticklabels([100,150,200,250])
# ax2.set_yticks(np.linspace(50, 200, 4))
# ax2.set_yticklabels([50, 100,150,200])
# ax3.set_yticks(np.linspace(10, 50, 5))
# ax3.set_yticklabels([10, 20,30,40,50])
# ax4.set_yticks(np.linspace(10, 50, 5))
# ax4.set_yticklabels([10, 20,30,40,50])
# ax5.set_yticks(np.linspace(10, 50, 5))
# ax5.set_yticklabels([10, 20,30,40,50])
# ax4.set_yticks(np.linspace(200, 1000, 5))
# ax4.set_yticklabels([200,400,600,800, 1000])
# ax5.set_yticks(np.linspace(25, 175, 7))
# ax5.set_yticklabels([25, 50,75,100,125,150,175])
# ax9.set_yticks(np.linspace(400000, 2000000, 5))
# ax9.set_yticklabels([400,800,1200, 1600, 2000])

ax6.set_yticks([])
ax6.set_yticklabels([])
# ax7.set_yticks([])
# ax7.set_yticklabels([])
# ax8.set_yticks([])
# ax8.set_yticklabels([])
# ax9.set_yticks([])
# ax9.set_yticklabels([])
# ax10.set_yticks([])
# ax10.set_yticklabels([])


ax1.plot(hour, grid_demand_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax1.plot(hour, grid_demand_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax1.plot(hour, grid_demand_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')
# ax1.legend(loc='upper left', fontsize='12', ncols=3)

# ax2.plot(hour, EV_demand_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax2.plot(hour, EV_demand_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax2.plot(hour, EV_demand_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')
# ax2.legend(loc='upper left', fontsize='12', ncols=3)

nada = np.zeros(24)
for i in range(24):
    nada[i] = 50
# ax3.plot(hour, der1, color='black', linestyle='--', label='RE generation', drawstyle='steps-post')
# ax3.plot(hour, offered_der11, color='limegreen', linestyle='--', label='offered RE', drawstyle='steps-post')
# ax3.plot(hour, offered_der12, color='magenta', linestyle='--', label='offered BESS', drawstyle='steps-post')



# ax3.plot(hour, der11_case2, color='blueviolet', label='RE supply', drawstyle='steps-post')
# ax3.plot(hour, der12_case2, color='steelblue', label='BESS supply', drawstyle='steps-post')


# ax3.plot(hour, der11, color='green', label='RE supply', drawstyle='steps-post')
# ax3.plot(hour, der12, color='darkred', label='BESS supply', drawstyle='steps-post')

#
# ax4.plot(hour, der2, color='black', linestyle='--', label='RE generation', drawstyle='steps-post')
# ax4.plot(hour, offered_der21, color='limegreen', linestyle='--', label='offered RE', drawstyle='steps-post')
# ax4.plot(hour, offered_der22, color='magenta', linestyle='--', label='offered BESS', drawstyle='steps-post')
# ax4.plot(hour, der21_case2, color='blueviolet', label='RE supply', drawstyle='steps-post')
# ax4.plot(hour, der22_case2, color='steelblue', label='BESS supply', drawstyle='steps-post')
#
# ax4.plot(hour, der21, color='green', label='RE supply', drawstyle='steps-post')
# ax4.plot(hour, der22, color='darkred', label='BESS supply', drawstyle='steps-post')
#
# ax5.plot(hour, der3, color='black', linestyle='--', label='RE generation', drawstyle='steps-post')
# ax5.plot(hour, offered_der31, color='limegreen', linestyle='--', label='offered RE', drawstyle='steps-post')
# ax5.plot(hour, offered_der32, color='magenta', linestyle='--', label='offered BESS', drawstyle='steps-post')
# ax5.plot(hour, nada, color='white', label=r'$k$'+'-double', drawstyle='steps-post')
#
# ax5.plot(hour, der31_case2, color='blueviolet', label='RE supply', drawstyle='steps-post')
# ax5.plot(hour, der32_case2, color='steelblue', label='BESS supply', drawstyle='steps-post')
# ax5.plot(hour, nada, color='white', label='CDA', drawstyle='steps-post')
#
# ax5.plot(hour, der31, color='green', label='RE supply', drawstyle='steps-post')
# ax5.plot(hour, der32, color='darkred', label='BESS supply', drawstyle='steps-post')
#
# ax5.legend(loc='upper left', fontsize='12', ncols=3)
# ax1.plot(date, ref_demand, color='black', linestyle='--', label='Without scheduling', alpha=0.6)
# ax1.plot(date, red_demand, color='darkred', linestyle='--', label='11 Mar start, 1x storage', alpha=0.8)
# ax1.plot(date, green_demand, color='green', linestyle='--', label='07 Feb start, 10x storage', alpha=0.7)
#
#
# ax2.set_ylabel('Cost (%)', fontproperties='Arial', size='11')  # we already handled the x-label with ax1
# ax2.plot(date, ref_cost, color='black', label='Without scheduling', alpha=0.6)
# ax2.plot(date, red_cost, color='darkred', label='11 Mar start, 1x storage', alpha=0.8)
# ax2.plot(date, green_cost, color='green', label='07 Feb start, 10x storage', alpha=0.7)

#
# ax2.arrow(310, 100, 0, -3, head_width = 3,
#          head_length=3, fc ='dimgray', ec ='dimgray')
#
# ax2.arrow(320, 100, 0, -35, head_width = 3,
#          head_length=3, fc ='dimgray', ec ='dimgray')
#
# ax1.legend(title='Aggregate Demand', loc='upper left', fontsize='8')
# ax2.legend(title='Cumulative Cost', loc='upper right', fontsize='8')
#
# ax2.text(288, 84, "   9%\nsaving")
# ax2.text(288, 65, "  38%\nsaving")

#fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('./Slides-grid-demand.png', dpi=300)
plt.show()