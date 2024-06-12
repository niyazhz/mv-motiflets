from os import listdir, getcwd, chdir
from os.path import isfile, join
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True


f_start = "motiflet_93_08_0"
save_name = "video_plot.pdf"
exp_path = "charleston_mini/"
x_lim = [450, 620]
y_lim = [530, 360]
title_fontsize = 28
label_fontsize = 20

video_path = exp_path + "video/"
files = [f for f in listdir(video_path) if isfile(join(video_path, f)) and f.startswith(f_start)]
files.sort()

#frames = [0, 4, 9, 14, 19, 24]
all_frame = list(range(25))
frames = [x for x in all_frame if x % 4 == 0]
#frames = all_frame[0::5]

size_y = len(files) * 2.2
size_x = len(frames) * 2
plt.rcParams['figure.figsize'] = [size_x, size_y]
outer = gridspec.GridSpec(len(files), 1, hspace = 0.1)

gs_list = []
for i, file in enumerate(files):
    gs_list.append(gridspec.GridSpecFromSubplotSpec(1, len(frames), subplot_spec = outer[i], wspace=0))

for i, gs in enumerate(gs_list):
    im = Image.open(video_path + files[i])
    for j, cell in enumerate(gs):
        ax = plt.subplot(cell)
        #if j == len(frames) - 1:
        if j == 0:
            ax.set_ylabel(f'Motif: {str(i+1)}', fontsize=label_fontsize)#, rotation=0, labelpad=35, fontsize=label_fontsize)
        if i == len(gs_list) - 1:
            frame = frames[j]
            ax.set_xlabel(f'Frame: {frame+1}', fontsize=label_fontsize)
        # Dicke der Ränder anpassen
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(1.5)  # Dicke auf 2.5 Punkte setzen
        im.seek(frames[j])
        ax.imshow(im)

        highlight_color = "red"
        highlight_linewidth = 3
        if i == 3:
            if j == 0:
                for pos in ['top', 'bottom', 'left']:
                    ax.spines[pos].set_edgecolor(highlight_color)
                    ax.spines[pos].set_linewidth(highlight_linewidth)
            elif j == len(frames) - 1:
                for pos in ['bottom', 'right', 'top']:
                    ax.spines[pos].set_edgecolor(highlight_color)
                    ax.spines[pos].set_linewidth(highlight_linewidth)
            else:
                for pos in ['bottom', 'top']:
                    ax.spines[pos].set_edgecolor(highlight_color)
                    ax.spines[pos].set_linewidth(highlight_linewidth)

        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_xticks([])
        ax.set_yticks([])

plt.suptitle("(d) 3d Illustration of the Individual Motifs (m=12, k=4)", y=0.93, fontsize=title_fontsize)
#plt.title("Test")
plt.savefig(exp_path + save_name, bbox_inches='tight')
plt.show()
