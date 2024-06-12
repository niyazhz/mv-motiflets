import scipy.io as sio

from motiflets.plotting import *

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import warnings

warnings.simplefilter("ignore")

import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 150

path = "datasets/experiments/"


def read_penguin_data():
    series = pd.read_csv(path + "penguin.txt",
                         names=(["X-Acc", "Y-Acc", "Z-Acc",
                                 "4", "5", "6",
                                 "7", "Pressure", "9"]),
                         delimiter="\t", header=None)
    ds_name = "Penguins (Longer Snippet)"

    return ds_name, series


def read_penguin_data_short():
    test = sio.loadmat(path + 'penguinshort.mat')
    series = pd.DataFrame(test["penguinshort"]).T
    ds_name = "Penguins (Snippet)"
    return ds_name, series


def test_plot_data():
    ds_name, series = read_penguin_data()
    series = series.iloc[497699 - 5000: 497699 + 5000, np.array([0, 7])].T

    ml = Motiflets(ds_name, series)
    ml.plot_dataset()


def test_univariate():
    ds_name, series = read_penguin_data_short()

    ml = Motiflets(
        ds_name, series,
        elbow_deviation=1,
        slack=0.8
    )
    # ml.plot_dataset()

    k_max = 50
    motif_length_range = np.arange(15, 50, 1)

    _, all_minima = ml.fit_motif_length(
        k_max, motif_length_range,
        plot_elbows=False,
        plot_motifsets=False,
        plot_best_only=True,
        subsample=1)

    ml.plot_motifset()


def test_multivariate():
    length = 2_000
    ds_name, B = read_penguin_data()

    for start in [0]:  # , 2000
        # dists = np.zeros(5)
        series = B.iloc[497699 + start:497699 + start + length, 0:4].T

        # for a, n_dims in enumerate(range(1, 6)):
        ml = Motiflets(ds_name, series,
                       n_dims=3
                       )

        k_max = 40
        motif_length_range = np.arange(20, 35, 1)

        best_length, _ = ml.fit_motif_length(
            k_max,
            motif_length_range,
            plot=True,
            plot_elbows=False,
            plot_motifsets=True,
            plot_best_only=True
        )
        # ml.plot_motifset()

        print("Best found length", best_length)


def test_plot_n_dim_plot():
    dists = [0., 25.16639805, 89.46489525, 137.10974884, 195.87618828]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Dimension Plot")
    sns.lineplot(x=np.arange(1, 6, dtype=np.int32), y=dists, ax=ax)
    plt.tight_layout()
    plt.show()


def test_univariate_profile():
    # ds_name, series = read_penguin_data_short()
    length = 2000
    B = pd.read_csv(path + "penguin.txt", delimiter="\t", header=None)
    ds_name = "Penguins (Longer Snippet)"
    df = B.iloc[497699: 497699 + length, 0:7].T

    ml = Motiflets(ds_name, df, elbow_deviation=1.25, slack=0.3)
    # ml.plot_dataset()

    k_max = 50
    motif_length_range = np.arange(10, 30, 1)

    _, all_minima = ml.fit_motif_length(
        k_max, motif_length_range,
        plot=False, plot_elbows=False, plot_motifsets=False,
        subsample=1)

    # ml.plot_motifset()


def test_multivariate_all():
    length = 2000
    ds_name, B = read_penguin_data()

    series = B.iloc[497699:497699 + length, 0:3].T
    ml = Motiflets(ds_name, series)

    k_max = 30
    motif_length_range = np.arange(20, 35, 1)

    best_length, _ = ml.fit_motif_length(
        k_max,
        motif_length_range,
        plot=False,
        plot_elbows=True,
        plot_motifsets=False,
    )
    ml.plot_motifset()

    print("Best found length", best_length)


def test_multivariate_niyaz():
    length = 2000
    ds_name, B = read_penguin_data()

    df = B.iloc[497699:497699 + length, 0:3].T
    ml = Motiflets(ds_name, df)

    k_max = 40
    motif_length = 22

    ml = Motiflets(ds_name, df,
                   slack=0.8,
                   dimension_labels=df.index
                   )
    
    ml.fit_k_elbow(k_max, motif_length=motif_length)

    ml.plot_motifset()


def test_multivariate_niyaz2():

    #ts = [[1,1,1,5,6,6,5,1,1,1,2,2,2,5,6,7,5,2,2,2,1,1,1,6,6,6,5,2,2,2],[0,0,0,7,6,6,7,0,0,0,1,1,1,6,6,6,7,1,1,1,0,0,0,7,6,6,6,1,1,1],[5,5,5,1,1,1,1,5,5,5,4,4,4,1,1,1,1,4,4,4,3,3,3,1,1,1,1,3,3,3]]
    
    ts = [[15, 16, 16, 5,6,6,5, 6, 17, 10, 18, 15, 17, 5,6,6,5,  4,  0, 10, 17,  3, 16, 5,6,6,5, 11, 17, 10],
          [13,  2,  2, 7,6,6,7, 9,  5, 12,  5, 11,  1, 7,6,6,7, 18,  7,  3, 11, 11,  0, 7,6,6,7,  2,  6,  4],
          [12, 10, 17,  9,  4,  7, 16, 10,  6, 12, 12,  9,  1, 15, 14,  6, 15, 11,  5,  4, 13, 13, 12,  7,  4, 11, 12,  6,  0, 14]]
    
    df = pd.DataFrame(ts)

    ds_name = "Test"

    ml = Motiflets(ds_name, df)

    k_max = 5
    motif_length = 4

    ml = Motiflets(ds_name, df,
                   slack=0.8,
                   dimension_labels=df.index,
                   n_dims=3
                   )
    
    #ml.fit_dims_elbow(k, motif_length=motif_length)
    ml.fit_k_elbow(k_max, motif_length=motif_length)

    ml.plot_motifset()

def test_multivariate_niyaz3():
    my_path = "datasets/ground_truth/"
    df = pd.read_csv(my_path + "vanilla_ice.csv", header=1)
    df = pd.DataFrame(df).T

    ds_name = "Toy Data"

    k_max = 10
    motif_length = 22

    ml = Motiflets(ds_name, df,
                   slack=0.8,
                   dimension_labels=df.index
                   )
    
    
    ml.fit_k_elbow(k_max, motif_length=motif_length)

    ml.plot_motifset()

test_multivariate_all()