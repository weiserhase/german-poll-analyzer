# Sonntagsfrage Poll Analysis "german-poll-anlyzer"

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Sonntagsfrage Poll Analysis** is a Python-based tool designed to scrape, analyze, and visualize polling data from [wahlrecht.de](https://www.wahlrecht.de/umfragen/insa.htm). It processes polling data for various political parties, generates insightful plots to track party performance over time, and computes minimal winning coalitions based on the latest poll results.

## Features

- **Data Scraping:** Automatically fetches and parses polling data from the specified website.
- **Data Processing:** Cleans and structures the data for analysis using pandas.
- **Visualization:** Generates time series plots for party polling trends and stacked bar charts for minimal winning coalitions.
- **Coalition Analysis:** Identifies and displays minimal winning coalitions based on customizable thresholds.
- **Customizable:** Easily adjust thresholds and excluded parties for coalition computations.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/sonntagsfrage-poll-analysis.git
    cd sonntagsfrage-poll-analysis
    ```

2. **Create a Virtual Environment (Optional but Recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script to scrape the latest polling data, generate visualizations, and compute minimal winning coalitions.

```bash
python poll_analysis.py
```

### Script Breakdown

- **Data Scraping and Processing**

    ```python
    import itertools
    import ssl
    from datetime import datetime
    
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from matplotlib.patches import Patch
    
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://www.wahlrecht.de/umfragen/insa.htm"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", class_="wilko")
    # ... [rest of the data scraping and processing code]
    ```

- **Visualization**

    ```python
    plt.figure(figsize=(12, 6))
    for party in parties_to_plot:
        latest_value = df_plot[party].tail(1).values[0]
        ls = "-" if latest_value > 5.0 else "--"
        plt.plot(df_plot.index, df_plot[party], label=party, color=party_colors.get(party, "gray"), linestyle=ls)
    # ... [rest of the plotting code]
    plt.show()
    ```

- **Coalition Analysis**

    ```python
    def minimal_winning_coalitions_for_row(row, threshold=45.0, exclude_parties=None, minimal_threshold=50.0):
        # ... [function implementation]
    
    winning_coalitions = minimal_winning_coalitions_for_row(
        df.iloc[-1], 
        threshold=45.0, 
        exclude_parties=parties_excluded_from_coalition
    )
    # ... [rest of the coalition analysis code]
    ```

## Dependencies

The project relies on the following Python libraries:

- `itertools`
- `ssl`
- `datetime`
- `matplotlib`
- `pandas`
- `requests`
- `beautifulsoup4`

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the [GNU V3](LICENSE).

