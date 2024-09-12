import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='13')
# --- FORMAT 1

df = pd.read_csv('./data/basic results/basic_results.csv')

# --- FORMAT 2</pre>
hour = df['hour']
grid_price = df['pi_g']
grid_mef = df['e_g']



fig, ax1 = plt.subplots\
    (nrows=1, subplot_kw=dict(frameon=False), figsize=(7, 5))

plt.subplots_adjust(hspace=.0, left=0.26, right=0.9, top=0.95, bottom=0.2)


ax1.set_ylabel('grid\n MEF\n(g.CO'+r'$_2$' + '/kWh)', fontproperties='Arial', size='16',
               rotation=0)
ax1.set_xlabel('time (hour)', fontproperties='Arial', size='16',
               rotation=0)
ax6 = ax1.twinx()

ax1.yaxis.set_label_coords(-0.24,0.4)

ax1.set_xlim([0, 25])

ax1.set_xticks(hour)
ax1.set_xticklabels(["", "2", "", "4", "", "6", "", "8", "", "10", "", "12", "", "14", "",
                     "16", "", "18", "", "20", "", "22", "", "24"])

ax1.set_ylim([280, 500])

ax1.set_yticks(np.linspace(300, 460, 5))
ax1.set_yticklabels([300, 340,380,420,460])

ax6.set_yticks([])
ax6.set_yticklabels([])

ax1.plot(hour, grid_mef, color='darkred', label='Baseline system')

#fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('./grid_mef.png', dpi=600)
plt.show()