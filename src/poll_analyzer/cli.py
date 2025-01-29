
import argparse

from poll_analyzer.coalition_analysis import minimal_winning_coalitions_for_row
from poll_analyzer.data_fetcher import fetch_html
from poll_analyzer.data_parser import parse_poll_data
from poll_analyzer.plotter import (plot_minimal_winning_coalitions,
                                   plot_timeseries)
from poll_analyzer.utils import PARTIES_TO_PLOT, PARTY_COLORS


def main():
    parser = argparse.ArgumentParser(
        prog="poll_analyzer",
        description="Analyze and visualize German poll data from wahlrecht.de"
    )
    subparsers = parser.add_subparsers(dest="command")

    # poll_analyzer show data
    show_parser = subparsers.add_parser("show", help="Show data or plots")
    show_parser.add_argument("subcommand", choices=["data", "plot"], help="Whether to show data or plots")

    # poll_analyzer coalition
    coalition_parser = subparsers.add_parser("coalition", help="Analyze coalitions")

    args = parser.parse_args()

    if args.command == "show":
        if args.subcommand == "data":
            show_data()
        elif args.subcommand == "plot":
            show_plot()

    elif args.command == "coalition":
        analyze_coalitions()
    else:
        parser.print_help()

def show_data():
    """
    Fetch the data and print it out in plain text.
    """
    html = fetch_html()
    df = parse_poll_data(html)
    print(df.tail(10))  # Show the latest 10 rows for brevity

def show_plot():
    """
    Fetch the data and show a timeseries plot.
    """
    html = fetch_html()
    df = parse_poll_data(html)
    plot_timeseries(df, PARTIES_TO_PLOT, PARTY_COLORS)

def analyze_coalitions():
    """
    Fetch data, compute minimal winning coalitions from the latest row, and plot them.
    """
    html = fetch_html()
    df = parse_poll_data(html)

    latest_poll = df.iloc[-1]
    coalitions = minimal_winning_coalitions_for_row(
        latest_poll,
        threshold=45.0, # Display Threshold
        exclude_parties=["Sonstige"],  # Example: Exclude 'Sonstige'
        minimal_threshold=50.0# Threshold for minimal coalitions
    )
    # Sort them descending by total
    coalitions_sorted = sorted(coalitions, key=lambda x: x[1], reverse=True)

    print("Minimal Winning Coalitions:")
    for coalition, total in coalitions_sorted:
        print(f"  {coalition} -> {total:.1f}%")
    print()

    # Plot
    plot_minimal_winning_coalitions(coalitions_sorted, latest_poll, PARTY_COLORS, threshold=50)

if __name__ == "__main__":
    main()