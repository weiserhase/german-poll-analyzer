import math
import os
import sys
import time
from dataclasses import dataclass
from typing import Optional, TypeVar

import keyboard

from poll_analyzer.utils.table_printer import Seperator, construct_table

A = TypeVar('A')  # Generic type for elements

def select_element_in_table(
    data: list[list[A]],
    header: str = "Select an element",
    sep: 'Seperator' = None,  
) -> A:
    """
    Allows selection of an element from a matrix of generic elements using keyboard or input.
    
    Args:
        data: Matrix of elements of type A
        header: Title to display above the table
        sep: Separator configuration for table rendering
        
    Returns:
        Selected element from the matrix
    """
    if sep is None:
        sep = Seperator()  
        
    max_r = len(data)
    max_c = max(len(row) for row in data) if data else 0
    selected_row = 0
    selected_col = 0
    keyboard_available = False

    try:
        keyboard.on_press_key("w", lambda _: None)
        keyboard.unhook_all()
        keyboard_available = True
    except:
        keyboard_available = False

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    def get_data_safe(data, row, col):
        try:
            return data[row][col]
        except IndexError:
            return None
        
    def handle_keyboard_input():
        nonlocal selected_row, selected_col
        
        key = keyboard.read_event(suppress=False)
        if key.event_type != 'down':  
            return None
        if key.name == 'w' or key.name == 'up':
            selected_row = (selected_row - 1) % max_r
        elif key.name == 's' or key.name == 'down':
            selected_row = (selected_row + 1) % max_r
        elif key.name == 'a' or key.name == 'left':
            selected_col = (selected_col - 1) % max_c
        elif key.name == 'd' or key.name == 'right':
            selected_col = (selected_col + 1) % max_c
        elif key.name == 'enter':
            return  get_data_safe(data, selected_row, selected_col)
        elif key.name == 'esc' or key.name == 'q':
            return False
            
        return None  

    def handle_text_input():
        nonlocal selected_row, selected_col
        
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
            return get_data_safe(data, selected_row, selected_col) 
        elif key == "q":
            return None
            
        return False  

    while True:
        clear_screen()
        print(header)
        lines = construct_table(
            data,
            sep,
            seperate_lines=False,
            highlight=(selected_row, selected_col),
        )
        for line in lines:
            print(line)

        if keyboard_available:
            print(
                "\nUse Arrow keys or WASD to move.\n"
                "Press Enter to select, or ESC/Q to quit.\n"
                f"Currently selected: (row={selected_row}, col={selected_col})"
            )
            result = handle_keyboard_input()
        else:
            print(
                "\nUse W/S to move up/down, A/D to move left/right.\n"
                "Press Enter to select, or 'q' to quit.\n"
                f"Currently selected: (row={selected_row}, col={selected_col})"
            )
            result = handle_text_input()
            
        if result is not None:  
            return result

        time.sleep(0.005)  # Small delay to prevent CPU overload

def organize_data(data: list[A], cols: Optional[int] = None, rows: Optional[int] = None) -> list[list[A]]:
    if not data:
        return [[]]
        
    total_elements = len(data)
    
    if cols is None and rows is None:
        cols = int(math.ceil(math.sqrt(total_elements)))
        rows = int(math.ceil(total_elements / cols))
    elif cols is None and rows is not None:
        cols = int(math.ceil(total_elements / rows))
    elif cols is not None and rows is None:
        rows = int(math.ceil(total_elements / cols))
        
    grid: list[list[A]] = [[] for _ in range(rows)]
    
    for i, element in enumerate(data):
        row_idx = i // cols
        if row_idx < rows:  
            grid[row_idx].append(element)
            
    max_cols = max(len(row) for row in grid)
    for row in grid:
        while len(row) < max_cols:
            row.append("")
            
    return grid
     
if __name__ == "__main__":
    table = organize_data([f"{i}" for i in range(1, 18)], cols=5)
    selected = select_element_in_table(table)
    print(selected)
    
    