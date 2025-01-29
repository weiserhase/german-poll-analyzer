
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def plot_timeseries(df, parties_to_plot, party_colors):
    """
    Plots the time series of poll data for specified parties.
    """
    df_plot = df[parties_to_plot].dropna(how="all")
    plt.figure(figsize=(12, 6))

    for party in parties_to_plot:
        if party not in df_plot.columns:
            continue
        latest_value = df_plot[party].dropna().tail(1)
        if latest_value.empty:
            linestyle = "--"
        else:
            val = latest_value.values[0]
            linestyle = "-" if val > 5.0 else "--"
        plt.plot(
            df_plot.index,
            df_plot[party],
            label=party,
            color=party_colors.get(party, "gray"),
            linestyle=linestyle
        )

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    plt.title("Sonntagsfrage - Parteiwerte über die Zeit")
    plt.xlabel("Datum")
    plt.ylabel("Umfragewerte in %")
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_minimal_winning_coalitions(coalitions, latest_poll, party_colors, threshold=50):
    """
    Plots minimal winning coalitions as stacked horizontal bars.
    `coalitions` should be a list of tuples ( (party1, party2, ...), total ).
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    y_positions = range(len(coalitions))

    for i, (parties, total) in enumerate(coalitions):
        left_edge = 0
        for p in parties:
            share = latest_poll[p]
            color = party_colors.get(p, "gray")
            # Mark as hatch if < 5%
            hatch = "///" if share < 5.0 else None
            ax.barh(
                i,
                share,
                left=left_edge,
                color=color,
                edgecolor='black',
                hatch=hatch
            )
            # Draw text on top
            ax.text(
                left_edge + share/2,
                i,
                f"{share:.1f}%",
                va='center',
                ha='center',
                color='white',
                fontsize=8
            )
            left_edge += share

        ax.text(
            left_edge + 1, i,
            f"Total: {total:.1f}%",
            va='center',
            fontsize=9,
            color='black'
        )

    # Y-axis labels
    labels = [", ".join(coal[0]) for coal in coalitions]
    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    # Draw vertical line for threshold
    ax.axvline(threshold, color="red", linestyle="--")

    ax.set_xlabel("Total %")
    ax.set_title("Minimal Winning Coalitions (≥50%) - Stacked by Party")

    # Construct legend
    legend_elements = [
        Patch(facecolor=party_colors[p], edgecolor='black', label=p)
        for p in latest_poll.index if p in party_colors
    ]
    hatch_elements = [
        Patch(facecolor='gray', edgecolor='black', hatch='///', label='Unter 5%')
    ]
    first_legend = ax.legend(
        handles=legend_elements,
        title='Parteien',
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )
    second_legend = ax.legend(
        handles=hatch_elements,
        title='Hinweise',
        bbox_to_anchor=(1.05, 0.8),
        loc='upper left'
    )
    ax.add_artist(first_legend)

    plt.tight_layout()
    plt.show()