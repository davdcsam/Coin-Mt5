# Standard
from threading import Thread
import time
from tkinter import filedialog as fd

# Third Party
from dearpygui.dearpygui import (
    get_value,
    set_value,
)

# import MetaTrader5 as mt5
from MetaTrader5 import initialize, login, last_error

# Owner
from src.logic.system_data import InternalData
from src.interface.terminal_output import output


class GetTerminal:
    """
    Class for managing a MetaTrader 5 terminal.
    """

    def __init__(self, input_fields, button_fields):
        self.dt = InternalData()
        self.input_fields = input_fields
        self.button_fields = button_fields

    def path_callback(self, sender, app_data):
        """
        Callback function for opening a file dialog to select a file.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        # Define the file types for the file dialog
        filetypes = (("Terminal", "terminal64.exe"), ("All files", "*.*"))

        # Open a file dialog and get the selected filename
        filename = fd.askopenfilename(
            title="Open a file", initialdir="C:/Program Files", filetypes=filetypes
        )

        # Set the value of the path input field to the selected filename
        set_value(self.dt.add_terminal_input_path["tag"], filename)

    def _connect_terminal_mt5(self):
        """
        Asynchronously initializes and logs into a MetaTrader 5 terminal.

        Args:
            path (str, required): The path to the MetaTrader64.exe file.
            user (int, required): The user ID for the terminal.
            password (str, required): The password for the user.
            server (str, required): The name of the server to connect to.
        Raises:
            mt5.error: If there's an issue with initializing
            or logging into the terminal.
        """
        """
        Try to initialize the MetaTrader 5 terminal
        with the provided parameters.
        """
        if not initialize(
            path=self.path,
            login=self.user,
            server=self.server,
            password=self.password,
            timeout=3000,
        ):
            print("Failed to initialize MetaTrader5", last_error())

        # Try to log into the terminal
        authorized = login(login=self.user, server=self.server, password=self.password)

        # If login is successful, change the connection status and print a success message
        if authorized:
            output(message=f"MetaTrader5 login successful {self.user}", f_type="t")
        else:
            # If login fails, print an error message with the error code
            output(f"MT5 {self.user} login failed, error code: {last_error()}", "t")

        time.sleep(0.1)

    def submit_connect_terminal_mt5(self):
        """
        Submits the form to connect to a MetaTrader 5 terminal.
        This method retrieves the user input from the form,
        uses it to connect to a MetaTrader 5 terminal asynchronously,
        and then deletes the form.
        """
        # Retrieve the user input from the form
        self.user = int(get_value(self.dt.add_terminal_input_user["tag"]))
        self.password = get_value(self.dt.add_terminal_input_password["tag"])
        self.server = get_value(self.dt.add_terminal_input_server["tag"])
        self.path = str(get_value(self.dt.add_terminal_input_path["tag"]))

        # Start a new thread to run the connect_terminal_mt5_async method
        Thread(target=self._connect_terminal_mt5).start()

    def clear_connect_terminal_mt5(self):
        """
        Clears the form to connect to a
        MetaTrader 5 terminal.
        This method sets the value of
        each input field in the form to an empty string.
        """
        # Iterate over the input fields and set their value to an empty string
        for field in self.input_fields:
            set_value(field["data"]["tag"], "")
