import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FixedLocator

title_fontsize = 20
label_fontsize = 16
marker_size = 8
line_width = 4

def highlight_cell(x,y, ax=None, **kwargs):
    rect = plt.Rectangle((x-.5, y-.5), 1,1, fill=False, **kwargs)
    ax = ax or plt.gca()
    ax.add_patch(rect)
    return rect

arr = np.array([[6,2,4,2,3,1,6,5,3,2,4,5,2,4]])
c_arr = np.zeros((len(arr),len(arr[0])))

plt.rcParams['figure.figsize'] = [11, 5]

fig, (ax1, ax2) = plt.subplots(2)
fig.subplots_adjust(hspace=-0.3)

# Definiere die Farben als [(Position, (R, G, B))]
colors = [(0, (1, 1, 1)), (1, (0.635, 0.698, 0.768))]  # Weiß und Hellblau
cmap_name = 'custom_cmap'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)

color1 = (0.635, 0.698, 0.768)
color2 = (0.098, 0.294, 0.478)

ax1.matshow(c_arr, cmap=custom_cmap) #"binary")
ax1.set_title("Time Series", fontsize=title_fontsize)
ax1.axes.get_xaxis().set_ticks([])
ax1.axes.get_yaxis().set_ticks([0])
ax1.set_yticklabels(["$T$"], fontsize=label_fontsize, rotation=90)


plt.grid(True, which="major")
plt.xlabel("$t$", fontsize=label_fontsize)

ax2.set_ylabel('$T$', fontsize=label_fontsize)
ax2.set_ylim([0, 7])
#ax2.set_xticklabels([])
ax2.set_axisbelow(True)
ax2.xaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
ax2.yaxis.set_major_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
ax2.grid(True, which="major")
ax2.plot(arr[0], color=color1)        
ax2.plot(arr[0], 'o', color=color2, linewidth=line_width, markersize=marker_size)

ax2.set_xticklabels([str(x) for x in range(1,len(arr[0])+1)])


for i in range(len(arr[0])):
    for j in range(len(arr)):
        c = arr[j,i]
        ax1.text(i, j, str(c), va='center', ha='center', fontsize="large") 
        highlight_cell(i, j, ax=ax1, color="black", linewidth=1)

plt.savefig('fundamentals/time_series.pdf', bbox_inches='tight', dpi=600)

plt.show()