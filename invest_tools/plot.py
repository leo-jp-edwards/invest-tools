import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_histogram(
    returns: pd.Series,
    percent_returns: pd.Series,
    plot_title: str,
    save: bool = False,
) -> None:
    axs = plt.figure(constrained_layout=True).subplots(1, 2)
    plots = [
        (axs[0], "Returns", returns, False),
        (axs[1], "Percent Returns", percent_returns, True),
    ]
    for ax, title, data, density in plots:
        ax.set(title=title)
        ax.hist(data, bins=75, density=density)
    if save:
        plt.savefig(plot_title)
    plt.show()


def plot_heatmap(matrix: pd.DataFrame, plot_title: str, save: bool = False) -> None:
    sns.heatmap(
        matrix,
        annot=True,
        cmap="YlGnBu",
        linewidth=0.3,
        annot_kws={"size": 9},
    )
    plt.xticks(rotation=90)
    plt.yticks(roations=0)
    if save:
        plt.savefig(plot_title)
    plt.show()
