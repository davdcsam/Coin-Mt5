# Standard
from asyncio import new_event_loop, set_event_loop
from json import load
from os import getcwd
import time
from tkinter import filedialog as fd
import webbrowser

# Third Party
from dearpygui.dearpygui import (
    add_button,
    add_child,
    add_input_text,
    add_table,
    add_table_column,
    add_table_row,
    add_menu,
    add_menu_item,
    add_text,
    add_viewport_menu_bar,
    delete_item,
    does_item_exist,
    get_value,
    set_value,
    window,
)

# import MetaTrader5 as mt5
from MetaTrader5 import initialize, login, last_error

# Owner
from src.logic.system_data import InternalData
from src.interface.terminal_output import output

data = InternalData()
error_table = [
    (10004, "REQUOTE", "Requote"),
    (10006, "REJECT", "Request rejected"),
    (10007, "CANCEL", "Request canceled by trader"),
    (10008, "PLACED", "Order placed"),
    (10009, "DONE", "Request completed"),
    (10010, "DONE_PARTIAL", "Only part of the request was completed"),
    (10011, "ERROR", "Request processing error"),
    (10012, "TIMEOUT", "Request canceled by timeout"),
    (10013, "INVALID", "Invalid request"),
    (10014, "INVALID_VOLUME", "Invalid volume in the request"),
    (10015, "INVALID_PRICE", "Invalid price in the request"),
    (10016, "INVALID_STOPS", "Invalid stops in the request"),
    (10017, "TRADE_DISABLED", "Trade is disabled"),
    (10018, "MARKET_CLOSED", "Market is closed"),
    (10019, "NO_MONEY", "There is not enough money to complete the request"),
    (10020, "PRICE_CHANGED", "Prices changed"),
    (10021, "PRICE_OFF", "There are no quotes to process the request"),
    (10022, "INVALID_EXPIRATION", "Invalid order expiration date in the request"),
    (10023, "ORDER_CHANGED", "Order state changed"),
    (10024, "TOO_MANY_REQUESTS", "Too frequent requests"),
    (10025, "NO_CHANGES", "No changes in request"),
    (10026, "SERVER_DISABLES_AT", "Autotrading disabled by server"),
    (10027, "CLIENT_DISABLES_AT", "Autotrading disabled by client terminal"),
    (10028, "LOCKED", "Request locked for processing"),
    (10029, "FROZEN", "Order or position frozen"),
    (10030, "INVALID_FILL", "Invalid order filling type"),
    (10031, "CONNECTION", "No connection with the trade server"),
    (10032, "ONLY_REAL", "Operation is allowed only for live accounts"),
    (10033, "LIMIT_ORDERS", "The number of pending orders has reached the limit"),
    (
        10034,
        "LIMIT_VOLUME",
        "The volume of orders and positions for the symbol has reached the limit",
    ),
    (10035, "INVALID_ORDER", "Incorrect or prohibited order type"),
    (
        10036,
        "POSITION_CLOSED",
        "Position with the specified POSITION_IDENTIFIER has already been closed",
    ),
    (
        10038,
        "INVALID_CLOSE_VOLUME",
        "A close volume exceeds the current position volume",
    ),
]


class GetTerminal:
    """
    Class for managing a MetaTrader 5 terminal.

    Attributes:
        terminal_data (dict): Data for the terminal loaded from a JSON file.
        input_fields (list): List of input fields for the terminal.
        button_fields (list): List of buttons for the terminal.
    """

    def __init__(self, file_path: str = f"{getcwd()}/data/terminal_data.json"):
        """
        Initializes the terminal with data from a JSON file.

        Args:
            file_path (str): Path to the JSON file with the terminal data.
        """
        # Load terminal data from the JSON file
        with open(file_path, "r") as file:
            self.terminal_data = load(file)
        # Define the input fields for the terminal with their default values
        self.input_fields = [
            {
                "data": data.add_terminal_input_user,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["user"],
            },
            {
                "data": data.add_terminal_input_password,
                "password": True,
                "default_value": self.terminal_data["ICMarkets"]["password"],
            },
            {
                "data": data.add_terminal_input_server,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["server"],
            },
            {
                "data": data.add_terminal_input_path,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["path"],
            },
        ]
        # Define the button fields for the terminal with their callbacks
        self.button_fields = [
            {
                "data": data.add_terminal_file_dialog_button,
                "callback": self.path_callback,
            },
            {
                "data": data.add_terminal_button_submit,
                "callback": self.submit_connect_terminal_mt5,
            },
            {
                "data": data.add_terminal_button_clear,
                "callback": self.clear_connect_terminal_mt5,
            },
            {
                "data": data.add_terminal_button_cancel,
                "callback": self.cancel_connect_terminal_mt5,
            },
        ]
        # Initialize the authorization status and the trade instance
        self.authorized = False

    def add_menu_bar(self):
        """
        Adds a menubar for terminal configuration.
        """
        # Create a new menu bar
        menu_bar = add_viewport_menu_bar()

        # Add menu items to the menu bar with their callbacks
        add_menu_item(
            label=data.add_terminal_button["label"],
            tag=data.add_terminal_button["tag"],
            parent=menu_bar,
            callback=self.add_terminal,
        )

        error_table_button = add_menu(
            tag=data.menu_error_table_button["tag"],
            label=data.menu_error_table_button["label"],
            parent=menu_bar,
        )

        def open_new_tab_web():
            webbrowser.open("https://www.mql5.com/en/docs/constants/errorswarnings")

        container_table = add_child(height=400, width=700, parent=error_table_button)
        add_button(
            label="Open Codes of Errors and Warnings",
            parent=container_table,
            callback=open_new_tab_web,
        )
        table = add_table(header_row=True, parent=container_table)
        add_table_column(label="Code", width_fixed=True, parent=table)
        add_table_column(label="TRADE_RETCODE", width_fixed=True, parent=table)
        add_table_column(label="Description", parent=table)

        for row in error_table:
            table_row = add_table_row(parent=table)
            add_text(str(row[0]), parent=table_row)
            add_text(row[1], parent=table_row)
            add_text(row[2], parent=table_row)

    def add_terminal(self):
        """
        Adds a window with input fields and buttons to the terminal.
        """
        # Create a new window with specific properties
        with window(
            label=data.add_terminal_window["label"],
            tag=data.add_terminal_window["tag"],
            autosize=True,
            no_collapse=True,
            no_close=True,
            no_title_bar=True,
        ):
            # Add a text field to the window
            add_text("Complete the form to add a terminal")

            # Add input fields to the window
            for field in self.input_fields:
                add_input_text(
                    label=field["data"]["label"],
                    tag=field["data"]["tag"],
                    no_spaces=True,
                    password=field["password"],
                    default_value=field["default_value"],
                )

            # Add buttons to the window
            for field in self.button_fields:
                add_button(
                    label=field["data"]["label"],
                    tag=field["data"]["tag"],
                    callback=field["callback"],
                )

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
        set_value(data.add_terminal_input_path["tag"], filename)

    async def connect_terminal_mt5_async(
        self, path: str, user: int, password: str, server: str
    ):
        """
        Asynchronously initializes and logs into a MetaTrader 5 terminal.

        Args:
            path (str, required): The path to the MetaTrader64.exe file.
            user (int, required): The user ID for the terminal.
            password (str, required): The password for the user.
            server (str, required): The name of the server to connect to.
        Raises:
            mt5.error: If there's an issue with initializing or logging into the terminal.
        """
        # Try to initialize the MetaTrader 5 terminal with the provided parameters
        if not initialize(
            path=path, login=user, server=server, password=password, timeout=3000
        ):
            print("Failed to initialize MetaTrader5", last_error())

        # Try to log into the terminal
        self.authorized = login(login=user, server=server, password=password)

        # If login is successful, change the connection status and print a success message
        if self.authorized:
            output(message=f"MetaTrader5 login successful {user}", f_type="t")
        else:
            # If login fails, print an error message with the error code
            output(f"MT5 {user} login failed, error code: {last_error()}", "t")

        time.sleep(0.1)

    def submit_connect_terminal_mt5(self):
        """
        Submits the form to connect to a MetaTrader 5 terminal.
        This method retrieves the user input from the form,
        uses it to connect to a MetaTrader 5 terminal asynchronously,
        and then deletes the form.
        """
        # Retrieve the user input from the form
        user = int(get_value(data.add_terminal_input_user["tag"]))
        password = get_value(data.add_terminal_input_password["tag"])
        server = get_value(data.add_terminal_input_server["tag"])
        path = str(get_value(data.add_terminal_input_path["tag"]))

        # Create a new event loop
        loop = new_event_loop()

        # Set the new event loop as the current event loop
        set_event_loop(loop)

        try:
            # Run the asynchronous function to connect to the terminal until it completes
            loop.run_until_complete(
                self.connect_terminal_mt5_async(path, user, password, server)
            )
        finally:
            # Close the event loop
            loop.close()

        # Delete the form
        delete_item(data.add_terminal_window["tag"])

    def clear_connect_terminal_mt5(self):
        """
        Clears the form to connect to a MetaTrader 5 terminal.
        This method sets the value of each input field in the form to an empty string.
        """
        # Iterate over the input fields and set their value to an empty string
        for field in self.input_fields:
            set_value(field["data"]["tag"], "")

    def cancel_connect_terminal_mt5(self):
        """
        Cancels the form to connect to a MetaTrader 5 terminal.
        This method stops the trade instance, changes the connection status,
        shuts down the terminal, and deletes the form.
        """
        try:
            # If the form exists, delete it
            if does_item_exist(data.add_terminal_window["tag"]):
                delete_item(data.add_terminal_window["tag"])
        except AttributeError:
            pass
