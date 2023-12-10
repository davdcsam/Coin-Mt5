# Standart
from json import load
from tkinter import filedialog
from pprint import pprint
from os import getcwd, path

# Third Party
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import (
    get_value,
    set_value,
)

# Owner
from src.logic.system_data import InternalData
from src.logic.print_output import output


# Exception class for handling invalid file formats
class InvalidFormatError(Exception):
    pass


# Main class for handling json operations and managing application settings
class RequiredLoadSaveTerminal:
    def __init__(self, input_fields) -> None:
        self.dt = InternalData()  # Instance of the InternalData class
        # Formats
        self.formats_json = ["user", "password", "server", "path"]
        self.input_fields = input_fields


class LoadTerminal(RequiredLoadSaveTerminal, InvalidFormatError):
    def __init__(self, input_fields) -> None:
        RequiredLoadSaveTerminal.__init__(self, input_fields)
        InvalidFormatError.__init__(self)

    def set_values(self, inputs, sender, app_data):
        for field in self.input_fields:
            data_value = field["data"]
            print(data_value)

    def read_file(self, sender, app_data, filename):
        # Check if a filename is provided
        if filename:
            # Open the file in read mode
            with open(filename, "r") as f:
                terminals_data = load(f)
                # Verify if the file has the correct format

            for terminal in terminals_data:
                print(terminal)
                for format_key in self.formats_json:
                    if format_key in terminals_data[terminal]:
                        continue
                    else:
                        print(f"'{format_key}' is not in '{terminal}'")
            # print(terminals_data)
            return terminals_data

    def load_file(self, sender, app_data):
        """
        Loads input field values from a file selected by the user.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        filename = f"{getcwd()}/data/terminal_data.json"
        try:
            terminals_data = self.read_file(
                filename=filename, sender=sender, app_data=app_data
            )
            # Set the values of the input fields to the inputs
            self.set_values(inputs=terminals_data, sender=sender, app_data=app_data)
        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to read the file
            print("You do not have permission to read the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while reading the file: {e}")
