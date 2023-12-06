# Standard
from datetime import datetime
from os import getcwd

# Third Party
# import pandas as pd
from pandas import DataFrame, isna

# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import add_text, get_item_width

# Owner
from src.logic.system_data import InternalData

dt = InternalData()
# Initializing a DataFrame with columns for datetime, type, and message
df = DataFrame(columns=["datetime", "type", "message"])

# Defining a dictionary to map format types to their respective string representations
format_type = {
    "w": "[WARNING]",
    "e": "[ERROR]",
    "t": "[TRADE]",
    "n": "[NOTE]",
    "s": "[SYSTEM]",
}

# Constructing the file path for the output CSV file
csv_file_path = getcwd() + "\\files\\output_terminal\\output_terminal-{}.csv".format(
    datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
)


# Defining a function to log a message with a specific format type
def output(message: str, f_type: str = "s"):
    """
    Logs a message with a specific format type.

    Args:
        f_type (str): The format type of the message.
            'w': [WARNING]
            'e': [ERROR]
            't': [TRADE]
            'n': [NOTE]
            's': [SYSTEM]
        message (str): The message to log.
    """
    # Creating a new row with the current datetime, format type, and message
    new_row = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": format_type[f_type],
        "message": message,
    }

    # Adding the new row to the DataFrame
    insert_loc = df.index.max()

    if isna(insert_loc):
        df.loc[0] = new_row
    else:
        df.loc[insert_loc + 1] = new_row

    # Saving the DataFrame to a CSV file
    df.to_csv(csv_file_path, mode="w")

    # Adding a new text widget for each message
    add_text(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {format_type[f_type]} {message}",
        parent=dt.terminal_output_window["tag"],
        wrap=get_item_width(dt.terminal_output_window["tag"]),
    )

    # Printing the message
    print(message)
