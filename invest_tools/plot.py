import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use("fivethirtyeight")


def plot_histogram(
    returns: pd.Series,
    percent_returns: pd.Series,
    plot_title: str,
    save: bool = False,
    save_location: str = None,
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
        plt.savefig(f"{save_location}/{plot_title}.png")
    plt.show()


def plot_heatmap(
    matrix: pd.DataFrame, plot_title: str, save: bool = False, save_location: str = None
) -> None:
    sns.heatmap(
        matrix,
        annot=True,
        cmap="YlGnBu",
        linewidth=0.3,
        annot_kws={"size": 9},
    )
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.title(plot_title)
    plt.tight_layout()
    if save:
        plt.savefig(f"{save_location}/{plot_title}.png")
    plt.show()


def plot_excess_returns(
    cumulative_returns: pd.DataFrame,
    plot_title: str,
    save: bool = False,
    save_location: str = None,
) -> None:
    cumulative_returns.plot(title=plot_title)
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2))
    plt.ylabel("Cumulative Returns")
    plt.tight_layout()
    if save:
        plt.savefig(f"{save_location}/{plot_title}.png")
    plt.show()
