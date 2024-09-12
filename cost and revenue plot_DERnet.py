import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='13')
# --- FORMAT 1
mpl.use('TkAgg')
df1 = pd.read_csv('./main_results.csv')
df = pd.read_csv('./community_data_25_17oct.csv')
#community_data_25_17oct
# --- FORMAT 2</pre>
hour = df1['hour']
cum_cost_baseline = df['cum_cost_baseline']
cum_cost_DER = df['cum_cost_DER']


cum_EI_baseline = df['cum_ei_baseline']
cum_EI_DER = df['cum_ei_DER']


cum_revenue_baseline = df['cum_revenue_baseline']
cum_revenue_DER = df['cum_revenue_DER']




fig, ax3 = plt.subplots\
    (subplot_kw=dict(frameon=False), figsize=(7, 4))

plt.subplots_adjust(hspace=.0, left=0.225, right=0.98, top=1, bottom=0.15)


# ax1.set_ylabel('cumulative\n emissions\n (kg.CO'+r'$_2$)', fontproperties='Arial', size='16', rotation=0)
# ax2.set_ylabel('cumulative\n cost\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)
ax3.set_ylabel('DER\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)


ax3.set_xlabel('time (hour)', fontproperties='Arial', size='16',
               rotation=0)
# ax4.set_ylabel('cumulative\n cost\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
# ax5.set_ylabel('cumulative\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
# ax6 = ax1.twinx()
# ax7 = ax2.twinx()
ax8 = ax3.twinx()

#ax9.set_ylabel('cumulative\n emissions\n (kg.CO'+r'$_2$)', fontproperties='Arial', size='11', rotation=0)

# ax1.yaxis.set_label_coords(-0.18,0.4)
# ax2.yaxis.set_label_coords(-0.18,0.4)
ax3.yaxis.set_label_coords(-0.18,0.4)


ax3.set_xlim([0, 25])
#plt.xticks(hour, hour, fontproperties='Arial', size = '16')
ax3.set_xticks(hour)
ax3.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])
#ax1.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
#                     "16", "17", "18", "19", "20", "21", "22", "23", "24"])


# ax1.set_ylim([0, 110])
# ax2.set_ylim([0, 100])
ax3.set_ylim([0, 25])




# ax1.set_yticks(np.linspace(20, 80, 4))
# ax1.set_yticklabels([20,40,60, 80])
# ax2.set_yticks(np.linspace(20, 100, 5))
# ax2.set_yticklabels([20,40,60, 80, 100])
ax3.set_yticks(np.linspace(5, 20, 4))
ax3.set_yticklabels([5, 10,15,20])

# ax4.set_yticks(np.linspace(200, 1000, 5))
# ax4.set_yticklabels([200,400,600,800, 1000])
# ax5.set_yticks(np.linspace(25, 175, 7))
# ax5.set_yticklabels([25, 50,75,100,125,150,175])
# ax9.set_yticks(np.linspace(400000, 2000000, 5))
# ax9.set_yticklabels([400,800,1200, 1600, 2000])

# ax6.set_yticks([])
# ax6.set_yticklabels([])
# ax7.set_yticks([])
# ax7.set_yticklabels([])
ax8.set_yticks([])
ax8.set_yticklabels([])



# ax1.plot(hour, cum_EI_baseline, color='darkred', label='Baseline', drawstyle='steps-post')
# ax1.plot(hour, cum_EI_DER, color='darkgreen', label='Proposed DERnet', drawstyle='steps-post')



# ax2.plot(hour, cum_cost_baseline, color='darkred', label='Baseline system', drawstyle='steps-post')
# ax2.plot(hour, cum_cost_DER, color='darkgreen', label='Proposed DERnet', drawstyle='steps-post')
#ax2.legend(loc='upper left', fontsize='16')

ax3.plot(hour, cum_revenue_baseline, color='darkred', label='Baseline system', drawstyle='steps-post')
ax3.plot(hour, cum_revenue_DER, color='darkgreen', label='Proposed DERnet', drawstyle='steps-post')
#ax3.legend(loc='upper left', fontsize='16')
ax3.legend(loc='upper left', fontsize='12', ncols=2)

#ax5.legend(loc='upper left', fontsize='16')


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
plt.savefig('./DERnet results3.png', dpi=300)
plt.show()