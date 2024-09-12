import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='13')
# --- FORMAT 1

df = pd.read_csv('./main_results.csv')
#community_data_25_17oct
# --- FORMAT 2</pre>
hour = df['hour']
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


fig, ax2 = plt.subplots\
    (subplot_kw=dict(frameon=False), figsize=(7, 4))

plt.subplots_adjust(hspace=.0, left=0.225, right=0.98, top=1, bottom=0.15)


#ax1.set_ylabel('cumulative\n emissions\n (kg.CO'+r'$_2$)', fontproperties='Arial', size='16', rotation=0)
ax2.set_ylabel('cumulative\n cost\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)
#ax3.set_ylabel('DER\n Type I\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)
#ax4.set_ylabel('DER\n Type II\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)
#ax5.set_ylabel('DER\n Type III\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='16', rotation=0)

ax2.set_xlabel('time (hour)', fontproperties='Arial', size='16',
               rotation=0)
# ax4.set_ylabel('cumulative\n cost\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
# ax5.set_ylabel('cumulative\n revenue\n ('+chr(163)+')', fontproperties='Arial', size='11', rotation=0)
#ax6 = ax1.twinx()
ax7 = ax2.twinx()
#ax8 = ax3.twinx()
#ax9 = ax4.twinx()
#ax10 = ax5.twinx()
#ax9.set_ylabel('cumulative\n emissions\n (kg.CO'+r'$_2$)', fontproperties='Arial', size='11', rotation=0)

#ax1.yaxis.set_label_coords(-0.2,0.4)
ax2.yaxis.set_label_coords(-0.2,0.4)
#ax3.yaxis.set_label_coords(-0.2,0.4)
#ax4.yaxis.set_label_coords(-0.2,0.4)
#ax5.yaxis.set_label_coords(-0.2,0.4)
# ax9.yaxis.set_label_coords(1.1,1)

ax2.set_xlim([0, 25])
#plt.xticks(hour, hour, fontproperties='Arial', size = '16')
ax2.set_xticks(hour)
ax2.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])
#ax1.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
#                     "16", "17", "18", "19", "20", "21", "22", "23", "24"])



#ax1.set_ylim([0, 2700000])
ax2.set_ylim([0, 1200])
#ax3.set_ylim([-5, 50])
#ax4.set_ylim([0, 220])
#ax5.set_ylim([-10, 50])

# ax1.set_yticks(np.linspace(400000, 2000000, 5))
# ax1.set_yticklabels([400,800,1200, 1600, 2000])
ax2.set_yticks(np.linspace(200, 1000, 5))
ax2.set_yticklabels([200,400,600,800, 1000])
# ax3.set_yticks(np.linspace(0, 40, 5))
# ax3.set_yticklabels([0, 10,20,30,40])
# ax4.set_yticks(np.linspace(30, 180, 6))
# ax4.set_yticklabels([30, 60,90,120,160,180])
# ax5.set_yticks(np.linspace(0, 40, 5))
# ax5.set_yticklabels([0, 10,20,30,40])
# ax4.set_yticks(np.linspace(200, 1000, 5))
# ax4.set_yticklabels([200,400,600,800, 1000])
# ax5.set_yticks(np.linspace(25, 175, 7))
# ax5.set_yticklabels([25, 50,75,100,125,150,175])
# ax9.set_yticks(np.linspace(400000, 2000000, 5))
# ax9.set_yticklabels([400,800,1200, 1600, 2000])

# ax6.set_yticks([])
# ax6.set_yticklabels([])
ax7.set_yticks([])
ax7.set_yticklabels([])
# ax8.set_yticks([])
# ax8.set_yticklabels([])
# ax9.set_yticks([])
# ax9.set_yticklabels([])
# ax10.set_yticks([])
# ax10.set_yticklabels([])


# ax1.plot(hour, cum_EI_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax1.plot(hour, cum_EI_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax1.plot(hour, cum_EI_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')
#ax1.legend(loc='upper left', fontsize='12', ncols=3)

ax2.plot(hour, cum_cost_case1, color='darkred', label='Baseline', drawstyle='steps-post')
ax2.plot(hour, cum_cost_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
ax2.plot(hour, cum_cost_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')

#
# ax3.plot(hour, cum_revenue1_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax3.plot(hour, cum_revenue1_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax3.plot(hour, cum_revenue1_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')

#
# ax4.plot(hour, cum_revenue2_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax4.plot(hour, cum_revenue2_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax4.plot(hour, cum_revenue2_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')

#
# ax5.plot(hour, cum_revenue3_case1, color='darkred', label='Baseline', drawstyle='steps-post')
# ax5.plot(hour, cum_revenue3_case2, color='blueviolet', label=r'$k$'+'-double auction', drawstyle='steps-post')
# ax5.plot(hour, cum_revenue3_CDA, color='darkgreen', label='Proposed CDA', drawstyle='steps-post')
ax2.legend(loc='upper left', fontsize='12', ncols=3)


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
plt.savefig('./slides-cost.png', dpi=300)
plt.show()