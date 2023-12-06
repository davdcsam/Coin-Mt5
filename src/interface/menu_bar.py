# Standart
from json import load
from os import getcwd
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
    add_text,
    add_viewport_menu_bar,
)

# Owner
from src.logic.system_data import InternalData
from src.logic.terminal_mt5 import GetTerminal


class MenuBar(GetTerminal):
    def __init__(self, file_path: str = f"{getcwd()}/data/terminal_data.json"):
        self.dt = InternalData()
        with open(file_path, "r") as file:
            self.terminal_data = load(file)
        self.add_terminal_input_fields = [
            {
                "data": self.dt.add_terminal_input_user,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["user"],
            },
            {
                "data": self.dt.add_terminal_input_password,
                "password": True,
                "default_value": self.terminal_data["ICMarkets"]["password"],
            },
            {
                "data": self.dt.add_terminal_input_server,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["server"],
            },
            {
                "data": self.dt.add_terminal_input_path,
                "password": False,
                "default_value": self.terminal_data["ICMarkets"]["path"],
            },
        ]
        self.add_terminal_button_fields = [
            {
                "data": self.dt.add_terminal_file_dialog_button,
                "callback": self.path_callback,
            },
            {
                "data": self.dt.add_terminal_button_submit,
                "callback": self.submit_connect_terminal_mt5,
            },
            {
                "data": self.dt.add_terminal_button_clear,
                "callback": self.clear_connect_terminal_mt5,
            },
        ]
        GetTerminal.__init__(
            self,
            input_fields=self.add_terminal_input_fields,
            button_fields=self.add_terminal_button_fields,
        )
        self.error_table = [
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
            (
                10022,
                "INVALID_EXPIRATION",
                "Invalid order expiration date in the request",
            ),
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
            (
                10033,
                "LIMIT_ORDERS",
                "The number of pending orders has reached the limit",
            ),
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

    def add(self):
        """
        Adds a menubar.
        """
        # Create a new menu bar
        menu_bar = add_viewport_menu_bar()

        # Add menu to the menu bar with their callbacks
        add_terminal = add_menu(
            label=self.dt.add_terminal_button["label"],
            tag=self.dt.add_terminal_button["tag"],
            parent=menu_bar,
        )

        add_text("Complete the form to add a terminal", parent=add_terminal)

        # Add input fields to the menu add terminal
        for field in self.add_terminal_input_fields:
            add_input_text(
                label=field["data"]["label"],
                tag=field["data"]["tag"],
                no_spaces=True,
                password=field["password"],
                default_value=field["default_value"],
                parent=add_terminal,
            )

        # Add buttons to the menu add terminal
        for field in self.add_terminal_button_fields:
            add_button(
                label=field["data"]["label"],
                tag=field["data"]["tag"],
                callback=field["callback"],
                parent=add_terminal,
            )

        error_table_button = add_menu(
            tag=self.dt.menu_error_table_button["tag"],
            label=self.dt.menu_error_table_button["label"],
            parent=menu_bar,
        )

        container_table = add_child(width=630, height=430, parent=error_table_button)

        add_button(
            label="Open Codes of Errors and Warnings",
            parent=container_table,
            callback=lambda: webbrowser.open(
                "https://www.mql5.com/en/docs/constants/errorswarnings"
            ),
        )

        table = add_table(header_row=True, parent=container_table)
        add_table_column(label="Code", width_fixed=True, parent=table)
        add_table_column(label="TRADE_RETCODE", width_fixed=True, parent=table)
        add_table_column(label="Description", width_fixed=True, parent=table)

        for row in self.error_table:
            table_row = add_table_row(parent=table)
            add_text(str(row[0]), parent=table_row)
            add_text(row[1], parent=table_row)
            add_text(row[2], parent=table_row)
