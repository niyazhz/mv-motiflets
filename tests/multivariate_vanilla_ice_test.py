import matplotlib as mpl
import motiflets.motiflets as mtfls

from tests.audio.lyrics import *

mpl.rcParams['figure.dpi'] = 300

path = "datasets/audio/"
ground_truth_path = "datasets/ground_truth/"

A_dataset = "Queen-David-Bowie-Under-Pressure"
A_ds_name = "Queen David Bowie - Under Pressure"

B_ds_name = "Vanilla Ice - Ice Ice Baby"
B_dataset = "Vanilla_Ice-Ice_Ice_Baby"
B_dataset_gt = "vanilla_ice_gt.csv"


datasets = [(A_dataset, A_ds_name), (B_dataset, B_ds_name)]
datasets = [(B_dataset, B_ds_name, B_dataset_gt)]

R_ds_name = "The Rolling Stones - Paint It, Black"
R_dataset = "The Rolling Stones - Paint It, Black"
R_dataset_gt = "rolling_gt.csv"

datasets = [(R_dataset, R_ds_name, R_dataset_gt)]

k_max = 25
length_in_seconds = 3.4  # in seconds
slack=0.6

def test_audio():
    for dataset, ds_name, B_dataset_gt in datasets:
        audio_file_url = path + dataset + ".mp3"
        audio_length_seconds, df, index_range = read_mp3(audio_file_url)
        channels = ['MFCC 0', 'MFCC 1', 'MFCC 2', 'MFCC 3']
        df = df.loc[channels]

        #gt = mtfls.read_ground_truth("vanilla_ice")

        # motif_length = int(length_in_seconds / audio_length_seconds * df.shape[1])
        # print("Length:", motif_length, "(", length_in_seconds, "s)")

        ml = Motiflets(ds_name, df,
                       # elbow_deviation=1.25,
                       dimension_labels=df.index
                       #slack=slack
                       #n_dims=2
                       )

        _, all_minima = ml.fit_motif_length(
            k_max, np.arange(150, 250, 10), subsample=1)

        for m in ml.motif_length_range[all_minima]:
            dists, motiflets, elbow_points = ml.fit_k_elbow(
                k_max,
                plot_elbows=False,
                plot_motifs_as_grid=False,
                motif_length=m)

            length_in_seconds = index_range[m]

            # best motiflet
            motiflet = np.sort(motiflets[elbow_points[-1]])
            print("Positions:", index_range[motiflet])

            path_ = "audio/snippets/" + ds_name + \
                    "_Channels_" + str(len(df.index)) + \
                    "_Length_" + str(m) + \
                    "_Motif.pdf"
            ml.plot_motifset(path=path_)

            extract_audio_segment(
                df, ds_name, audio_file_url, "snippets/queen-vanilla-ice",
                length_in_seconds, index_range, m, motiflet)


def test_consensus():
    k_max = 40

    df_consensus = None
    audio_length_seconds = 0
    for dataset, ds_name in datasets:
        audio_file_url = path + dataset + ".mp3"
        seconds, df, index_range = read_mp3(audio_file_url)
        audio_length_seconds += seconds
        channels = ['MFCC 2', 'MFCC 3']
        df = df.loc[channels]

        if df_consensus is None:
            df_consensus = df
        else:
            df = pd.concat([df_consensus, df], axis=1)
            df.columns = np.arange(0, df.shape[1]) * audio_length_seconds / df.shape[1]

    ds_name = "Consensus"
    motif_length = 120  # int(length_in_seconds / audio_length_seconds * df.shape[1])
    print(motif_length, length_in_seconds, "s")

    ml = Motiflets(ds_name, df,
                   # elbow_deviation=1.25,
                   slack=0.9,
                   dimension_labels=df.index,
                   )

    dists, motiflets, elbow_points = ml.fit_k_elbow(
        k_max,
        motif_length=motif_length,
        slack=0.9,
        plot_elbows=True,
        plot_grid=False)

    # best motiflet
    motiflet = np.sort(motiflets[elbow_points[-1]])
    print("Positions:", motiflet)

    path_ = "audio/snippets/queen-vanilla-ice/" + ds_name + "_Channels_" + str(
        len(df.index)) + "_Motif.pdf"
    ml.plot_motifset(path=path_)

    # extract_audio_segment(
    #     df, ds_name, audio_file_url, "snippets/queen-vanilla-ice",
    #     length_in_seconds, index_range, motif_length, motiflet)

test_audio()
