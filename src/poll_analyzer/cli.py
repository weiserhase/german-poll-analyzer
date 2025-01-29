
import argparse
import time

from poll_analyzer.coalition_analysis import minimal_winning_coalitions_for_row
from poll_analyzer.config import PARTIES_TO_PLOT, PARTY_COLORS, URLS
from poll_analyzer.data_fetcher import fetch_html
from poll_analyzer.data_parser import parse_poll_data
from poll_analyzer.plotter import (plot_minimal_winning_coalitions,
                                   plot_timeseries)
from poll_analyzer.utils.select_element import (organize_data,
                                                select_element_in_table)


def main():
    options = {
            "Show Data": show_data,
            "Show Plot": show_plot,
            "Coalition ": analyze_coalitions,
            "Quit": lambda x:  exit(),        }
    while True: 
        selection = select_element_in_table(organize_data(options.keys(), 1), header="Select an option")
        if selection == "Quit":
            break
        source = select_element_in_table(organize_data(URLS.keys(), 1), header="Select a pollster to analyze")
        source_url = URLS[source]
        options[selection](source_url)
def show_data(url):
    """
    Fetch the data and print it out in plain text.
    """
    html = fetch_html( url=url)
    df = parse_poll_data(html)
    print(df.tail(10))  # Show the latest 10 rows for brevity
    while input("Press 'q' to continue...") !="q":
        time.sleep(0.5)
        continue   

def show_plot(url):
    """
    Fetch the data and show a timeseries plot.
    """
    html = fetch_html(url)
    df = parse_poll_data(html)
    plot_timeseries(df, PARTIES_TO_PLOT, PARTY_COLORS)

def analyze_coalitions(url):
    """
    Fetch data, compute minimal winning coalitions from the latest row, and plot them.
    """
    html = fetch_html(url)
    df = parse_poll_data(html)

    latest_poll = df.iloc[-1]
    coalitions = minimal_winning_coalitions_for_row(
        latest_poll,
        threshold=47.5, # Display Threshold
        exclude_parties=["Sonstige"],  # Example: Exclude 'Sonstige'
        minimal_threshold=50.0 # Threshold for minimal coalitions
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