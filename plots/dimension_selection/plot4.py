import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FixedLocator
import matplotlib.gridspec as gridspec
import random
import motiflets as mtf

plt.rcParams['figure.figsize'] = [11, 9]

title_fontsize = 20
label_fontsize = 16
marker_size = 8
line_width = 4

def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect

def compute_relevant_dimensions(D_full, knns, k, use_dim):
    last_knns = knns[:,:,k-1]
    last_knns_distance = np.take_along_axis(D_full, last_knns[:,:,None], axis=2)
    argsort_last_knns = np.argsort(last_knns_distance, axis=0)[:use_dim]

    best_dims = argsort_last_knns.transpose(1, 0, 2).reshape(argsort_last_knns.shape[1], use_dim)
    return best_dims 


arr = np.array([[2,2,5,5,2,2,6,6,2,2,4,4,2,2], [2,2,6,3,2,2,4,3,2,2,5,3,2,2], [6,2,4,2,3,1,6,5,3,2,4,5,2,4]])
#c_arr = np.zeros((len(arr),len(arr[0])))


s_len = 4
k_max = 3
k = k_max
D_full, knns = mtf.compute_distance_matrix(
        arr, s_len, k_max,
        slack=0.5,
        sum_dims=False)
        
#knns_original = knns

#indexing from 1
#knns = knns_original + 1

last_knns = knns[:,:,k-1]
last_knns_distance = np.take_along_axis(D_full, last_knns[:,:,None], axis=2)
use_dim = 2
argsort_last_knns = np.argsort(last_knns_distance, axis=0)[:use_dim]
best_dims = argsort_last_knns.transpose(1, 0, 2).reshape(argsort_last_knns.shape[1], use_dim)

arr = best_dims + 1
#arr = arr.round(1)
c_arr = np.zeros((len(arr),len(arr[0])))
print(arr)

i_color = [k_max-1, k_max]

for i in range(len(c_arr)):
    for j in range(len(c_arr[0])):
        if j >= i_color[0] and j <= i_color[1]:
            #c_arr[i,j] = 1
            pass

#make outer gridspec
fig = plt.figure()

ax1 = plt.subplot()


color1 = (0.635, 0.698, 0.768)
color2 = (0.098, 0.294, 0.478)
colors = [(0, (1, 1, 1)), (1, (0.635, 0.698, 0.768, 0.5))]  # Weiß und Hellblau
cmap_name = 'custom_cmap'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)

ax1.matshow(c_arr, cmap=custom_cmap) #"binary")
#ax1.set_title("Multivariate Subsequence", fontsize=title_fontsize)
ax1.axes.get_xaxis().set_ticks(range(0,2))
ax1.axes.get_yaxis().set_ticks(range(0,11))
#ax1.set_yticklabels(['$T^{(1)}$', '$T^{(2)}$', '$T^{(3)}$'], fontsize=label_fontsize, rotation=90)
ax1.set_xticklabels([str(x) for x in range(1,3)], fontsize=16)
ax1.set_yticklabels([str(y) for y in range(1,12)], fontsize=16)
ax1.tick_params(top=False, labeltop=False, bottom=True, labelbottom=True, )

for i in range(len(arr[0])):
    for j in range(len(arr)):
        c = arr[j,i]
        ax1.text(i, j, str(c), va='center', ha='center', fontsize="xx-large") 
        highlight_cell(i, j, ax=ax1, color="black", linewidth=1)

#plt.grid(True, which="major")
#plt.xlabel("$t$", fontsize=label_fontsize)

#plt.subplots_adjust(top = 0, bottom = 0, right = 0, left = 0)

plt.savefig(f'dimension_selection/plot4/plot4.png', bbox_inches='tight', pad_inches = 0, dpi=400)
plt.show()