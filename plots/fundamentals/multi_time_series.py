import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FixedLocator
import matplotlib.gridspec as gridspec
import random

title_fontsize = 20
label_fontsize = 16
marker_size = 8
line_width = 4

def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect


arr = np.array([[2,2,5,5,2,2,6,6,2,2,4,4,2,2], [2,2,6,3,2,2,4,3,2,2,5,3,2,2], [6,2,4,2,3,1,6,5,3,2,4,5,2,4]])
c_arr = np.zeros((len(arr),len(arr[0])))


plt.rcParams['figure.figsize'] = [11, 9]

#make outer gridspec
fig = plt.figure()
outer = gridspec.GridSpec(2, 1, figure=fig, height_ratios = [1, 2], hspace = 0.05) 

#make nested gridspecs
gs1 = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec = outer[0])
gs2 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec = outer[1], hspace = 0.15)

ax1 = plt.subplot(gs1[0])
ax2 = plt.subplot(gs2[0])
ax3 = plt.subplot(gs2[1])
ax4 = plt.subplot(gs2[2])

color1 = (0.635, 0.698, 0.768)
color2 = (0.098, 0.294, 0.478)
colors = [(0, (1, 1, 1)), (1, (0.635, 0.698, 0.768, 0.5))]  # Weiß und Hellblau
cmap_name = 'custom_cmap'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)

ax1.matshow(c_arr, cmap=custom_cmap) #"binary")
ax1.set_title("Multivariate Time Series", fontsize=title_fontsize)
ax1.axes.get_xaxis().set_ticks([])
ax1.axes.get_yaxis().set_ticks([0,1,2])
ax1.set_yticklabels(['$T^{(1)}$', '$T^{(2)}$', '$T^{(3)}$'], fontsize=label_fontsize, rotation=90)

for i in range(len(arr[0])):
    for j in range(len(arr)):
        c = arr[j,i]
        ax1.text(i, j, str(c), va='center', ha='center', fontsize="large") 
        highlight_cell(i, j, ax=ax1, color="black", linewidth=1)

plt.grid(True, which="major")
plt.xlabel("$t$", fontsize=label_fontsize)

ax2.set_ylabel('$T^{(1)}$', fontsize=label_fontsize)
ax2.set_ylim([0, 7])
ax2.set_xticklabels([])
ax2.set_axisbelow(True)
ax2.xaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
ax2.yaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
ax2.grid(True, which="major")
ax2.plot(arr[0], color=color1)        
ax2.plot(arr[0], 'o', color=color2, linewidth=line_width, markersize=marker_size)

ax3.set_ylabel('$T^{(2)}$', fontsize=label_fontsize)
ax3.set_ylim([0, 7])
ax3.set_xticklabels([])
ax3.set_axisbelow(True)
ax3.xaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
ax3.yaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
ax3.grid(True, which="major")
ax3.plot(arr[1], color=color1)        
ax3.plot(arr[1], 'o', color=color2, linewidth=line_width, markersize=marker_size)

ax4.set_ylabel('$T^{(3)}$', fontsize=label_fontsize)
ax4.set_ylim([0, 7])
ax4.set_axisbelow(True)
ax4.xaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
ax4.yaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
ax4.grid(True, which="major")
ax4.plot(arr[2], color=color1)        
ax4.plot(arr[2], 'o', color=color2, linewidth=line_width, markersize=marker_size)

ax4.set_xticklabels([str(x) for x in range(1,len(arr[0])+1)])

plt.savefig('fundamentals/multi_time_series.pdf', bbox_inches='tight', dpi=600)

plt.show()