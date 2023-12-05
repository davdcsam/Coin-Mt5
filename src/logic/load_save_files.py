# Standart
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
from src.interface.terminal_output import output

data = InternalData()


class InvalidFormatError(Exception):
    """
    Exception raised when the file format is invalid.
    """

    pass


class RequiredLoadSaveFiles:
    def __init__(self) -> None:
        self.filedailog_filetypes = (("Set Files", "*.set"), ("All files", "*.*"))
        self.categories = {
            "Trade": [
                "select_type",
                "lot_size",
                "stop_loss",
                "take_profit",
                "magic_number",
                "deviation_trade",
            ],
            "Section Time": [
                "section_time_start",
                "section_time_end",
            ],
            "Start Section": [
                "start_hour",
                "start_min",
                "start_sec",
            ],
            "End Section": [
                "end_hour",
                "end_min",
                "end_sec",
            ],
        }
        self.last_input_filename = f"{getcwd()}/data/last_inputs.set"


class LoadFiles(InvalidFormatError, RequiredLoadSaveFiles):
    def __init__(self, trade_instance) -> None:
        InvalidFormatError.__init__(self)
        RequiredLoadSaveFiles.__init__(self)
        self.trade_instance = trade_instance

    def set_values(self, inputs, sender, app_data):
        """
        Sets the values of the input fields in the window.

        Args:
            inputs (dict): Dictionary of input field values.
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        # Verify if inputs is a dict
        if not isinstance(inputs, dict):
            return

        # Verify no extra inputs
        for key in list(inputs.keys()):
            # If key is not in categories list, it'll pop element in inputs arg
            if not any(key in category for category in self.categories.values()):
                inputs.pop(key)

        # Iterate over the inputs
        for key, value in inputs.items():
            # Get the component associated with the key
            component = data.__getattr__(f"set_input_{key}")
            # Get the default type of the component
            default_type = type(get_value(component["tag"]))

            # print(f"\n{key} {value}")
            # print(f"{type(key)} {type(value)} default type={default_type}\n")

            # Check if the type of the value matches the default type
            if not isinstance(value, default_type):
                try:
                    # Try to convert the value to the default type
                    value = default_type(value)
                    # Set the value of the component
                    set_value(component["tag"], value)
                    output(
                        message="Set {} to {}".format(
                            value, data.__getattr__(f"set_input_{key}")["label"]
                        )
                    )
                except ValueError:
                    """
                    Print an error message if the value could not be converted
                    """
                    pprint(
                        f"Could not convert {value} to type {default_type}\n",
                        f"Could not set {value} to {component['label']}",
                    )
                    continue
                except TypeError:
                    pprint(f"Widget {key} {value} doesn't exist")
                    continue
            elif isinstance(value, str):
                set_value(component["tag"], value)
                output(
                    message="Set {} to {}".format(
                        value, data.__getattr__(f"set_input_{key}")["label"]
                    )
                )
            elif isinstance(value, dict):
                # Convert the value of the dict to a integer
                for var in value:
                    value[var] = int(value[var])
                # Set the value of the component
                set_value(component["tag"], value)
                output(
                    message="Set {}:{}:{} to {}".format(
                        value["hour"],
                        value["min"],
                        value["sec"],
                        data.__getattr__(f"set_input_{key}")["label"],
                    )
                )

    def read_file(self, filename, sender, app_data):
        """
        Reads input field values from a file.

        Args:
            filename (str): Path to the file.
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.

        Returns:
            dict: Dictionary of input field values.
        """
        # Check if a filename is provided
        if filename:
            # Open the file in read mode
            with open(filename, "r", encoding="utf-16") as f:
                # Initialize a dictionary to store the inputs
                inputs = {}
                # Iterate over the lines in the file
                for line in f:
                    # Strip whitespace from the line
                    line = line.strip()
                    # Check if the line contains an equals sign
                    if "=" in line:
                        # If it does, split the line into a key and value
                        key, value = line.split("=")
                    else:
                        # If it doesn't, skip the line
                        continue
                    # Add the key and value to the inputs dictionary
                    inputs[key] = value

                # Verify if the file has the correct format
                required_keys = [
                    name
                    for category in self.categories.values()
                    for name in category
                    if name not in ["section_time_end", "section_time_start"]
                ]
                for key in required_keys:
                    if key not in inputs:
                        raise self.InvalidFormatError(
                            f"The file does not contain the required key: {key}"
                        )

                # Convert the select_type to a int
                temp_select_type = None

                for key, value in self.trade_instance.order_types_dict.items():
                    if int(inputs["select_type"]) == value:
                        temp_select_type = key

                # Update the inputs dictionary
                inputs.update(
                    {
                        "select_type": temp_select_type,
                        "section_time_start": {
                            "hour": inputs.pop("start_hour"),
                            "min": inputs.pop("start_min"),
                            "sec": inputs.pop("start_sec"),
                        },
                        "section_time_end": {
                            "hour": inputs.pop("end_hour"),
                            "min": inputs.pop("end_min"),
                            "sec": inputs.pop("end_sec"),
                        },
                    }
                )
            output(f"\n          Loading inputs from {path.basename(filename)}", "s")
            return inputs

    def load_file(self, sender, app_data):
        """
        Loads input field values from a file selected by the user.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            # Open a file dialog for the user to select a file to load from
            filename = filedialog.askopenfilename(
                title="Open",
                initialdir=f"{getcwd()}/files/set_input",
                filetypes=self.filedailog_filetypes,
                defaultextension=".set",
            )
            # Read the inputs from the selected file
            inputs = self.read_file(filename=filename, sender=sender, app_data=app_data)

            # Set the values of the input fields to the inputs
            self.set_values(inputs=inputs, sender=sender, app_data=app_data)
        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to read the file
            print("You do not have permission to read the file.")
        except self.InvalidFormatError as e:
            # Print an error message if the file format is invalid
            print(str(e))
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while reading the file: {e}")

    def load_last_inputs(self, sender, app_data):
        """
        Loads the last input field values from a file.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            # Read the inputs from the last input file
            inputs = self.read_file(
                filename=self.last_input_filename, sender=sender, app_data=app_data
            )
            # Set the values of the input fields to the inputs
            self.set_values(inputs, sender, app_data)
        except FileNotFoundError:
            # Print an error message if the file was not found
            print("Last inputs was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to read the file
            print("You do not have permission to read the file.")
        except self.InvalidFormatError as e:
            # Print an error message if the file format is invalid
            print(str(e))
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while reading the file: {e}")

    def load_symbols(self, filename: str = "symbols.txt"):
        filepath = path.join(getcwd(), "data", filename)

        if not path.exists(filepath):
            print(f"The file {filepath} does not exist.")
            return ["US30", "BCHUSD"]

        try:
            with open(filepath, "r") as f:
                symbols = [line.strip() for line in f.readlines()]
        except IOError as e:
            print(f"An error occurred while opening the file: {str(e)}")
            return ["US30", "BCHUSD"]

        if len(symbols) == 0:
            symbols.append("BCHUSD")
            symbols.append("US30")

        return symbols


class SaveFiles(InvalidFormatError, RequiredLoadSaveFiles):
    def __init__(self, trade_instance) -> None:
        InvalidFormatError.__init__(self)
        RequiredLoadSaveFiles.__init__(self)
        self.trade_instance = trade_instance

    def get_values(self, sender, app_data):
        """
        Retrieves the values of the input fields in the window.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.

        Returns:
            dict: Dictionary of input field values.
        """
        # Initialize a dictionary to store the tags
        tags = {}
        # Iterate over the categories
        for category in self.categories.values():
            # Iterate over the names in each category
            for name in category:
                # Check if the name is in the data
                if f"set_input_{name}" in data.get_all():
                    # If it is, add it to the tags dictionary
                    tags[name] = data.__getattr__(f"set_input_{name}")["tag"]
                else:
                    # If it's not, add a default value to the tags dictionary
                    tags[name] = "0"

        # Get the values for each tag
        values = {name: get_value(tag) for name, tag in tags.items()}

        # Update the values
        if values["select_type"] != "":
            values.update(
                {
                    "select_type": self.trade_instance.order_types_dict[
                        values["select_type"]
                    ]
                }
            )
        else:
            values.update({"select_type": 0})

        values.update(
            {
                "start_hour": values["section_time_start"]["hour"],
                "start_min": values["section_time_start"]["min"],
                "start_sec": values["section_time_start"]["sec"],
                "end_hour": values["section_time_end"]["hour"],
                "end_min": values["section_time_end"]["min"],
                "end_sec": values["section_time_end"]["sec"],
            }
        )
        # Initialize a dictionary to store the result
        result = {}
        # Iterate over the categories and names
        for category, names in self.categories.items():
            for key in [category] + [
                name
                for name in names
                if name not in ["section_time_end", "section_time_start"]
            ]:
                # Check if the key is a category
                if key in self.categories:
                    # If it is, add a semicolon to the result dictionary
                    result[key] = ";"
                else:
                    # If it's not, get the value for the key
                    value = values.get(key, "")
                    # Check the type of the value and add it to the result dictionary
                    if value is None:
                        result[key] = 0
                    elif value is True:
                        result[key] = int(value)
                    elif value is False:
                        result[key] = int(value)
                    else:
                        result[key] = str(value)
        # Return the result dictionary
        return result

    def write_file(self, filename, data, sender, app_data):
        """
        Writes input field values to a file.

        Args:
            filename (str): Path to the file.
            data (dict): Dictionary of input field values.
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        # Check if a filename is provided
        if filename:
            # Open the file in write mode
            with open(filename, "w", encoding="utf-16") as f:
                # Iterate over the data
                for key, value in data.items():
                    # Check if the value is a semicolon
                    if value == ";":
                        # If it is, write a comment line to the file
                        f.write(f"; {key}\n")
                    else:
                        # If it's not, write a line with the key and value to the file
                        f.write(f"{key}={value}\n")

    def save_file(self, sender, app_data):
        """
        Saves input field values to a file selected by the user.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            # Get the values from the form
            data = self.get_values(sender=sender, app_data=app_data)
            # Open a file dialog for the user to select a file to save to
            filename = filedialog.asksaveasfilename(
                title="Save as",
                initialdir=f"{getcwd()}/files/set_input",
                filetypes=self.filedailog_filetypes,
                defaultextension=".set",
            )
            # Write the data to the selected file
            self.write_file(
                filename=filename, data=data, sender=sender, app_data=app_data
            )
            # Print a success message
            output(message=f"Save inputs on {self.last_input_filename}")
        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while writing to the file: {e}")

    def save_last_inputs(self, sender, app_data):
        """
        Saves the last input field values to a file.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            # Get the values from the form
            data = self.get_values(sender=sender, app_data=app_data)
            # Write the data to the last input file
            self.write_file(
                filename=self.last_input_filename,
                data=data,
                sender=sender,
                app_data=app_data,
            )
        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while writing to the file: {e}")
