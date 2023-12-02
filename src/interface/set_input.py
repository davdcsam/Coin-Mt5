# Standard
from tkinter import filedialog
from pprint import pprint
from threading import Thread
from os import getcwd

# Third Party
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import (
    add_combo,
    add_text,
    add_input_float,
    add_input_int,
    add_time_picker,
    add_button,
    get_value,
    set_value,
)

# Owner
from src.interface.base_component import BaseComponent
from src.interface.set_font import Fonts
from src.logic.system_data import InternalData
from src.interface.terminal_output import output
from src.logic.trade import Trade

data = InternalData()
fonts_instance = Fonts()


class SetInput(BaseComponent):
    """
    Class for setting input fields in a DearPyGUI window.

    Attributes:
        sections (list): List of sections to be added to the window.
        filedailog_filetypes (tuple): File types for
          the file dialog.
        categories (dict): Categories of input fields.
        last_input_filename (str): Path to the last inputs file.
    """

    class InvalidFormatError(Exception):
        """
        Exception raised when the file format is invalid.
        """

        pass

    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes the input fields in a DearPyGUI window.

        Args:
            tag (str): Unique label for the component.
            parent (str): Label of the parent component.
        """
        super().__init__(tag, parent, **kwargs)
        self.sections = [
            ("title", None),
            ("title_data_trade", self.data_trade),
            ("title_section_time", self.section_time),
            (None, self.load_save),
            ("title_bot_manager", self.bot_manager),
        ]
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
        self.trade_instance = Trade()

    def add(self):
        """
        Adds sections and a load/save button to the window.
        """
        # Iterate over the sections
        for section, function in self.sections:
            """
            If a sections is diferent to None,
            add a text field to the window for each section.
            And set the title font
            """
            if section is not None:
                add_text(
                    data.__getattr__(f"set_input_text_{section}")["label"],
                    tag=data.__getattr__(f"set_input_text_{section}")["tag"],
                    parent=self.window,
                )
                fonts_instance.set_font_item(
                    data.__getattr__(f"set_input_text_{section}")["tag"]
                )

            """
            If a function is provided for the section,
            call it with the window as the parent
            """
            if function is not None:
                function(parent=self.window)

    def data_trade(self, parent):
        """
        Adds data trade input fields to the window.

        Args:
            parent: The parent widget.
        """
        self.list_order_type = [key for key in self.trade_instance.order_types_dict.keys()]

        self.add_components(
            ["set_input_select_type"],
            add_combo,
            width=200,
            items=self.list_order_type,
        )

        self.add_components(
            ["set_input_lot_size", "set_input_stop_loss", "set_input_take_profit"],
            add_input_float,
            width=200,
        )
        self.add_components(
            ["set_input_magic_number", "set_input_deviation_trade"],
            add_input_int,
            width=200,
        )

    def section_time(self, parent):
        """
        Adds time section input fields to the window.

        Args:
            parent: The parent widget.
        """
        self.add_components(
            ["set_input_section_time_start", "set_input_section_time_end"],
            add_time_picker,
            hour24=True,
        )

    def load_save(self, parent):
        """
        Adds load and save buttons to the window.

        Args:
            parent: The parent widget.
        """
        self.add_components(
            ["set_input_button_load"],
            add_button,
            callback=self.load_file,
        )
        self.add_components(
            ["set_input_button_save"],
            add_button,
            callback=self.save_file,
        )

    def bot_manager(self, parent):
        self.add_components(
            ["set_input_button_deploy"],
            add_button,
            callback=self.start_trade_instance,
        )
        self.add_components(
            ["set_input_button_undeploy"],
            add_button,
            callback=self.trade_instance.stop,
            show=False,
        )

    def start_trade_instance(self, sender, app_data):
        """
        Starts the trade instance in a new thread.
        """
        """
        Create a new thread that will run the
        start method of the trade instance.
        """
        thread = Thread(
            target=self.trade_instance.start,
            args=(self.get_values(sender, app_data),),
        )
        # Start the new thread
        thread.start()

    ###########################################################################

    def set_values(self, inputs, sender, app_data):
        """
        Sets the values of the input fields in the window.

        Args:
            inputs (dict): Dictionary of input field values.
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        # Iterate over the inputs
        for key, value in inputs.items():
            # Get the component associated with the key
            component = data.__getattr__(f"set_input_{key}")
            # Get the default type of the component
            default_type = type(get_value(component["tag"]))
            # Check if the type of the value matches the default type
            if type(value) is not default_type and default_type is not type(None):
                try:
                    # Try to convert the value to the default type
                    print(key, value)
                    value = default_type(value)
                    # Set the value of the component
                    set_value(component["tag"], value)
                    # Print a message indicating the value has been set
                    output(message=f"Set {value} to {key}")
                except ValueError:
                    """
                    Print an error message if the value could not be converted
                    """
                    pprint(
                        f"Could not convert {value} to type {default_type}\n",
                        f"Could not set {value} to {component['label']}",
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
                # Update the inputs dictionary with the start and end times
                inputs.update(
                    {
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
            # Return the inputs dictionary
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

    ##########################################################################

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

        # Update the values dictionary with the start and end times
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
