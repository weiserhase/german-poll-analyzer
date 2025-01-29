
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup


def parse_poll_data(html: str) -> pd.DataFrame:
    """
    Parse the wahlrecht.de poll HTML and return a DataFrame of poll results.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="wilko")
    if not table:
        raise ValueError("Could not find the table with class 'wilko' in the HTML.")
    
    # Extract headers
    header_row = table.find("thead").find("tr")
    headers = [th.get_text(strip=True) for th in header_row.find_all("th")]

    # Identify relevant columns by name
    party_columns = {
        label: idx for idx, label in enumerate(headers)
        if label in ["CDU/CSU", "SPD", "GRÜNE", "FDP", "LINKE", "AfD", "FW", "BSW", "Sonstige"]
    }

    # Iterate over table rows
    data = []
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        # Skip rows that do not have enough columns
        if len(cells) < 14:
            continue

        date_text = cells[0].get_text(strip=True)
        try:
            poll_date = datetime.strptime(date_text, "%d.%m.%Y").date()
        except ValueError:
            # If date parsing fails, skip row
            continue

        row_data = {"Date": poll_date}
        # Parse columns for each party
        for party, col_index in party_columns.items():
            val = cells[col_index].get_text(strip=True)
            if val in ["–", ""]:
                pct = None
            else:
                val = val.replace("%", "").replace(",", ".")
                try:
                    pct = float(val)
                except ValueError:
                    pct = None
            row_data[party] = pct

        data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data)
    df.sort_values(by="Date", inplace=True)
    df.set_index("Date", inplace=True)

    return df