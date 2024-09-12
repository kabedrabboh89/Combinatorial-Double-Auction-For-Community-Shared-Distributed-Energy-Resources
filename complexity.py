import matplotlib.pyplot as plt

import pandas as pd
import matplotlib as mpl
mpl.rc('font',family='Arial', size='11')
import numpy as np
# --- FORMAT 1

df = pd.read_csv('./complexity.csv')

# --- FORMAT 2</pre>
n = df['number of consumers']
n = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000]
time = df['time']

fig, ax = plt.subplots(figsize=(7, 5))

plt.subplots_adjust(hspace=.0, top=0.98, bottom=0.2)


ax.set_ylabel('computation \ntime (s)', fontproperties='Arial', size='16')


#ax.yaxis.set_label_coords(-0.2,0.4)

#ax.set_xlim([0, 100000])
plt.xscale("log")
ax.set_xticks(n)
ax.set_xticklabels([r'$10^2$', "", "", "", "", "", "", "", "", r'$10^3$', "", "",
                   "", r'$5x10^3$'])
ax.set_xlabel('number of consumers', fontproperties='Arial', size='16')
ax.set_ylim([0, 95])

ax.set_yticks(np.linspace(10, 90, 9))
ax.set_yticklabels(["10", "20", "30", "40", "50", "60", "70", "80", "90"])

ax.get_xaxis().get_major_formatter().labelOnlyBase = False


ax.plot(n, time, color='darkred', label='without CDA', linestyle='--', marker='d')


#fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('./complexity.png', dpi=600)
plt.show()