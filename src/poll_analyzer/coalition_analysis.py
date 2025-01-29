
import itertools

import pandas as pd


def minimal_winning_coalitions_for_row(
    row: pd.Series,
    threshold: float = 50.0,
    exclude_parties=None,
    minimal_threshold: float = 50.0
):
    """
    Given a row of poll data (parties -> percentage),
    return minimal winning coalitions that reach or exceed `threshold` (default 50%).
    
    A coalition is 'minimal' if removing any party from it drops below `minimal_threshold`.
    """
    if exclude_parties is None:
        exclude_parties = []

    # Filter out excluded parties and drop any NaN
    row_cleaned = row.dropna().drop(labels=exclude_parties, errors='ignore')
    parties = row_cleaned.index
    
    valid_coalitions = []
    for r in range(1, len(parties) + 1):
        for combo in itertools.combinations(parties, r):
            total_percentage = row_cleaned[list(combo)].sum()
            if total_percentage >= threshold:
                # Check minimal condition
                is_minimal = True
                for party in combo:
                    if (total_percentage - row_cleaned[party]) >= minimal_threshold:
                        is_minimal = False
                        break
                if is_minimal:
                    valid_coalitions.append((combo, total_percentage))

    return valid_coalitions