# Standard
from datetime import datetime
from os import getcwd

# Third Party
# import pandas as pd
from pandas import DataFrame, isna
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import add_text, get_value, set_value

# Owner
from src.interface.base_component import BaseComponent
from src.logic.system_data import InternalData

data = InternalData()
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

# Getting the tag container from the terminal output text container
tag_container = data.terminal_output_text_container["tag"]


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

    # Getting the current console output
    console_output = get_value(tag_container)

    # If there is console output, append the new message to it
    if console_output is not None:
        console_output += "{} {} {}\n".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), format_type[f_type], message
        )

        # Setting the value of the tag container to the updated console output
        set_value(tag_container, console_output)

        # Printing the message
        print(message)


# Defining a class to manage terminal output in a DearPyGUI window
class TerminalOutput(BaseComponent):
    """
    Class for managing terminal output in a DearPyGUI window.

    Attributes:
        sections (list): List of sections to be added to the window.
        filedailog_filetypes (tuple): File types for the file dialog.
        categories (dict): Categories of input fields.
        last_input_filename (str): Path to the last inputs file.
    """

    # Initializing the terminal output in a DearPyGUI window
    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes the terminal output in a DearPyGUI window.

        Args:
            tag (str): Unique label for the component.
            parent (str): Label of the parent component.
        """
        super().__init__(tag, parent, **kwargs)

    # Adding sections and a load/save button to the window
    def add(self):
        """
        Adds sections and a load/save button to the window.
        Also created a csv file where is saved outputs.
        """
        self.add_components(["terminal_output_text_container"], add_text)

        # Creating a CSV file for the terminal output
        self._create_terminal_output_csv()

    # Creating a CSV file for the terminal output
    def _create_terminal_output_csv(self):
        """
        Creates a CSV file for the terminal output.
        """
        return df.to_csv(csv_file_path, mode="w")

    # Logging an internal output message
    def _internal_output(self, sender, app_data):
        """
        Logs an internal output message.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        # Creating a new row with the current datetime, format type, and message
        new_row = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": format_type["n"],
            "message": get_value(sender),
        }

        # Adding the new row to the DataFrame
        df.loc[len(df)] = new_row

        # Saving the DataFrame to a CSV file
        df.to_csv(csv_file_path, mode="w")

        # Getting the current console output and appending the new message to it
        console_output = (
            get_value(tag_container)
            + f"{datetime.now()} {format_type['n']} {get_value(sender)}\n"
        )

        # Setting the value of the tag container to the updated console output
        set_value(tag_container, console_output)
