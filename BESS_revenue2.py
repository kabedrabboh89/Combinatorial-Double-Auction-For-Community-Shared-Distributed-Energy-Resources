import numpy as np
import matplotlib as mpl
mpl.rc('font',family='Arial', size=16)
import matplotlib.pyplot as plt
import pandas as pd


x_labels = ["50", "100", "150", "200", "250"]
y_labels = ["140", "130", "120", "110", "100"]

revenue = np.zeros((5, 5), dtype=float)
charging_re = np.zeros((5, 5), dtype=float)

df_data = pd.read_csv('./DER2/revenue.csv')

y = ["1.4", "1.3", "1.2", "1.1", "1"]
j = 0
for i in y:
    revenue[j] = df_data[i]
    j += 1


print(revenue)
fig, ax = plt.subplots(figsize=(7, 5.25))
plt.subplots_adjust(left=0.16, right=0.84, top=0.98, bottom=0.17)
im = ax.imshow(revenue, cmap='RdYlGn')

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.linspace(0, 4, 5))
ax.set_yticks(np.linspace(0, 4, 5))

ax.set_xticklabels(x_labels)
ax.set_yticklabels(y_labels)

ax.set_xlabel('consumers\' average EI weight\n' +r'$\gamma_{avg}$' + ' (' + chr(163) + '/tonne.CO'+r'$_2eq$)')
ax.set_ylabel('RE price as a percentage\n of grid price (%)')

cbar = fig.colorbar(im)
cbar.set_label('revenue ('+chr(163)+')', rotation=90)
# Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")

#Loop over data dimensions and create text annotations.
# for i in range(5):
#      for j in range(5):
#         text = ax.text(j, i, round(charging_re[i, j]),
#                         ha="center", va="center", color="w")

#ax.set_title("IC check")
fig.tight_layout()
plt.savefig('./revenue_price.png', dpi=600)
plt.show()