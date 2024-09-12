import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

###  initialisation  ###

df = pd.read_csv('./network_data.csv')
weights = df['resistance']
pos_df = pd.read_csv('./node_pos.csv')
#labels = pos_df['consumers']
pos_df = pos_df[['node', 'xpos', 'ypos']]
pos = pos_df.set_index('node').T.to_dict('list')

G = nx.Graph()

G = nx.from_pandas_edgelist(df, 'nodeA', 'nodeB', 'resistance')
#pos = nx.kamada_kawai_layout(G)  # positions for all nodes - seed for reproducibility

def Resistance(target, source):
    return nx.shortest_path_length(G, source=source, target=target, weight='resistance')

#print(G)
#nodes
nx.draw_networkx_nodes(G, pos, node_size=100)

# edges
nx.draw_networkx_edges(G, pos, width=1)
#print(list(G))

# node labels
nx.draw_networkx_labels(G, pos, font_size=8, font_color='white', font_family="Arial")
# edge weight labels
# edge_labels = nx.get_edge_attributes(G, "distance")
# #nx.draw_networkx_edge_labels(G, pos, edge_labels)
#
# x = np.linspace(0, 5, 100)
# N = 8
#
# # colormap
# cmap = plt.get_cmap('Dark2', N)
#
# # Normalizer
# norm = mpl.colors.Normalize(vmin=0, vmax=7)
#
# # creating ScalarMappable
# sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
# sm.set_array([])
#
# plt.colorbar(sm, ticks=[], orientation='horizontal')
#
# ax = plt.gca()
# ax.margins(0.08)
# plt.axis("off")
#
plt.tight_layout()
plt.show()
#
# plt.savefig('./network.png', dpi=600)