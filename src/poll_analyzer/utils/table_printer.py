import time
from dataclasses import dataclass
from functools import partial
from typing import Any, Optional


@dataclass(frozen=True)
class Seperator:
    vertical: str = "|"
    horizontal: str = "-"
    intersection: str = "+"

def calculate_width(data: list[list[Any]]) -> list[int]:
    row_item_widths: list[list[int]] = [[] for _ in range(len(data[0]))]
    for row in data:
        for i, element in enumerate(row):
            row_item_widths[i].append(len(f"{element}"))
    return [max(col) for col in row_item_widths]

def fetch_entry(row: int, col: int, data: list[list[Any]]) -> Any:
    if len(data) <= row or row < 0:
        return ""
    if len(data[row]) <= col or col < 0:
        return ""
    return data[row][col]

def seperator(col_widths: list[int], sep: Seperator) -> str:
    elements: list[str] = []
    for width in col_widths:
        elements.append(sep.horizontal * (width + 2))
    return sep.intersection + sep.intersection.join(elements) + sep.intersection

def construct_row(
    row: list[Any],
    row_idx: int,
    col_widths: list[int],
    sep: Seperator,
    highlight: Optional[tuple[int, int]] = None,
) -> str:
    """
    Constructs a single row of the table.
    If highlight is (h_row, h_col) and row_idx == h_row, then the h_col cell is highlighted.
    """
    elements: list[str] = []
    for col_idx, element in enumerate(row):
        text = f"{element}"
        padding = " " * (col_widths[col_idx] - len(text))

        # Check if we should highlight this cell
        if highlight is not None and row_idx == highlight[0] and col_idx == highlight[1]:
            # Simple highlight using ANSI inverse video
            cell_str = f"\033[7m {text}{padding} \033[0m"
        else:
            cell_str = f" {text}{padding} "

        elements.append(cell_str)

    return f"{sep.vertical}{sep.vertical.join(elements)}{sep.vertical}"

def max_bounds(data: list[list[Any]]) -> tuple[int, int]:
    return len(data), max([len(row) for row in data])

def construct_table(
    data: list[list[Any]],
    sep: Seperator,
    seperate_lines: bool = False,
    highlight: Optional[tuple[int, int]] = None,
) -> list[str]:
    max_r, max_c = max_bounds(data)
    updated_data = [
        [fetch_entry(j, i, data) for i in range(max_c)] for j in range(max_r)
    ]
    col_width = calculate_width(updated_data)
    constructed_seperator = seperator(col_width, sep)

    output: list[str] = [constructed_seperator]
    for row_i, row in enumerate(updated_data):
        if "__sep" in row:
            output.append(constructed_seperator)
            continue
        output.append(
            construct_row(
                row, 
                row_i, 
                col_width, 
                sep, 
                highlight=highlight
            )
        )
        if seperate_lines and row_i != len(data) - 1:
            output.append(constructed_seperator)
    output.append(constructed_seperator)
    return output

def print_table(
    data: list[list[Any]],
    sep: Seperator = Seperator()  # noqa: B008
) -> None:
    lines = construct_table(data, sep, False)
    print("\n".join(lines), flush=True)

def select_element_in_table[A](
    data: list[A],
    header: str = "Select an element",
    sep: Seperator = Seperator(),
) -> A:
    max_r, max_c = max_bounds(data)
    selected_row = 0
    selected_col = 0
    
    while True:
        print("\033[H\033[J", end="")
        fo 
        lines = construct_table(
            data,
            sep,
            seperate_lines=False,
            highlight=(selected_row, selected_col),
        )
        for line in lines:
            print(line)

        print(
            "Use W/S to move up/down, A/D to move left/right.\n"
            "Press Enter to select, or 'q' to quit.\n"
            f"Currently selected: (row={selected_row}, col={selected_col})"
        )

        key = input(">> ").lower().strip()
        if key == "w":
            selected_row = (selected_row - 1) % max_r
        elif key == "s":
            selected_row = (selected_row + 1) % max_r
        elif key == "a":
            selected_col = (selected_col - 1) % max_c
        elif key == "d":
            selected_col = (selected_col + 1) % max_c
        elif key == "":
            # Interpreted as "Enter"
            return (selected_row, selected_col)
        elif key == "q":
            return (-1, -1)


if __name__ == "__main__":
    # Example data
    config = [
        ["Coin", "Amount", "Euro Value"],
        ["__sep"],
        ["BTC", 0.18576332, 4136],
        ["ETH", round(270.35 / 1537.9, 5), 270.35],
        ["__sep"],
        ["XMR", round(172.367 / 141.9, 5), 172.367],
    ]
    
    # Demonstrate printing the table once
    print_table(config)

    # Demonstrate selecting a cell from the table
    row, col = select_element_in_table(config)
    if row == -1 and col == -1:
        print("Selection canceled.")
    else:
        selected_value = fetch_entry(row, col, config)
        print(f"You selected row={row}, col={col} which contains: '{selected_value}'")

    # (Optional) Sleep or do other logic afterward
    time.sleep(1)