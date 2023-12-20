# Standard
from threading import Thread
import time
from pprint import pprint

# Third Party
import MetaTrader5 as mt5
import pandas as pd

# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import show_item, hide_item, enable_item, disable_item

# Owner
from src.logic.print_output import output, save_csv_when_stop, output_dict_request
from src.logic.system_data import InternalData

"""
Dont implement dt has a atr into Trade class, 'cuase when
thread _method start take dt has a Dict incallable,
also can create a Picking Error.
"""
dt = InternalData()


class SectionTime:
    """
    This class represents a time section. It has methods to initialize the section,
    check if a given time falls within the section, and verify if there are no positions
    for a given symbol within the section.
    """

    def __init__(self) -> None:
        """
        Initializes the SectionTime object with default values.
        """
        self.section_time_state = False
        self.section_time_no_position_flag = False
        self.total_positions_magic_symbol = None
        self.positions_symbols_magic = {}

    def section_time_oninit(self, inputs: dict):
        """
        Initializes the start and end times of the section from the input dictionary.
        If the end time is earlier than the start time, they are swapped.
        """
        # Extracting the start and end times from the input dictionary
        self.local_start_hour = int(inputs["start_hour"])
        self.local_start_min = int(inputs["start_min"])
        self.local_start_sec = int(inputs["start_sec"])
        self.local_end_hour = int(inputs["end_hour"])
        self.local_end_min = int(inputs["end_min"])
        self.local_end_sec = int(inputs["end_sec"])
        self.magic_number = int(inputs["magic_number"])

        # Swapping the start and end times if the end time is earlier
        if (
            self.local_end_hour < self.local_start_hour
            or (
                self.local_end_hour == self.local_start_hour
                and self.local_end_min < self.local_start_min
            )
            or (
                self.local_end_hour == self.local_start_hour
                and self.local_end_min == self.local_start_min
                and self.local_end_sec < self.local_start_sec
            )
        ):
            temp_hour = self.local_start_hour
            temp_min = self.local_start_min
            temp_sec = self.local_start_sec

            self.local_start_hour = self.local_end_hour
            self.local_start_min = self.local_end_min
            self.local_start_sec = self.local_end_sec
            self.local_end_hour = temp_hour
            self.local_end_min = temp_min
            self.local_end_sec = temp_sec

    def section_time_ontick(self, time_broker: time.struct_time):
        """
        Checks if the given time falls within the start and end times of the section.
        Updates the section_time_state accordingly.
        """
        # Checking if the given time is after the start time
        if (
            time_broker.tm_hour > self.local_start_hour
            or (
                time_broker.tm_hour == self.local_start_hour
                and time_broker.tm_min > self.local_start_min
            )
            or (
                time_broker.tm_hour == self.local_start_hour
                and time_broker.tm_min == self.local_start_min
                and time_broker.tm_sec >= self.local_start_sec
            )
        ):
            # Checking if the given time is before the end time
            if (
                time_broker.tm_hour < self.local_end_hour
                or (
                    time_broker.tm_hour == self.local_end_hour
                    and time_broker.tm_min < self.local_end_min
                )
                or (
                    time_broker.tm_hour == self.local_end_hour
                    and time_broker.tm_min == self.local_end_min
                    and time_broker.tm_sec <= self.local_end_sec
                )
            ):
                self.section_time_state = True
            else:
                self.section_time_state = False
        else:
            self.section_time_state = False

    def section_time_verify_no_position_flag(self, symbol: str = None):
        """
        Verifies if there are no positions for the given symbol within the section.
        Updates the section_time_no_position_flag accordingly.
        """
        # Getting the positions for the given symbol
        positions_symbol = mt5.positions_get(symbol=symbol)

        """
        Checking if there are no positions for the given symbol,
        set the section_time_no_position_flag to Tru
        """
        if len(positions_symbol) == 0:
            pprint(f"No positions in {symbol}")
            self.section_time_no_position_flag = True
        # Otherwise create a dataframe with open positions in the symbol.
        else:
            self.df_positions_symbol = pd.DataFrame(
                list(positions_symbol),
                columns=positions_symbol[0]._asdict().keys(),
            )
            # Check if these positions have the same magic number to create a new child dataframe.
            df_positions_symbol_magic_zero = self.df_positions_symbol[
                self.df_positions_symbol["magic"] == self.magic_number
            ]
            # Check if this child dataframe is empty to set the flag to True.
            if len(df_positions_symbol_magic_zero) == 0:
                self.section_time_no_position_flag = True
            else:
                self.section_time_no_position_flag = False


class Trade(SectionTime):
    """
    The Trade class is a subclass of SectionTime,designed to manage trading threads in a separate thread.
    It handles the initialization, execution, and deinitialization of trades, and provides real-time updates on the trading thread.
    """

    def __init__(self) -> None:
        super().__init__()
        self.thread = None
        self.running = False
        self.symbol = "EURUSD"
        self.order_types_dict: dict[str, int] = {
            "Buy": mt5.ORDER_TYPE_BUY,
            "Sell": mt5.ORDER_TYPE_SELL,
        }
        self.first_trade_flag = True

    def required_initializer(self) -> None:
        """
        Establishes connection to the MetaTrader 5 terminal and enables the
        display of the self.symbol in MarketWatch.
        If any of these operations fail, it stops the thread and quits.
        """
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            output(f"Initialize failed, error code: {mt5.last_error()}", "e")
            self.stop()
            quit()

        # Attempt to enable the display of the self.symbol in MarketWatch
        selected = mt5.symbol_select(self.symbol, True)
        if not selected:
            output(f"Failed to select {self.symbol}")
            self.stop()
            quit()

        self.symbol_info = mt5.symbol_info(self.symbol)

        if self.symbol_info is None:
            output(
                f"{self.symbol} not found, cannot check orders. {mt5.last_error()}", "e"
            )
            self.stop()
            quit()

        info_terminal = mt5.terminal_info()

        if not info_terminal.trade_allowed:
            output(
                f"Algo Traiding is Disable. Please, Turn On. {mt5.last_error()}", "e"
            )
            return False

        if info_terminal.tradeapi_disabled:
            output(
                f"Sorry, Broker blocked connection to MT5 API. {mt5.last_error()}", "e"
            )
            return False

        return True

    def _build_request(self):
        """
        Prepare a trade request with the necessary parameters
        """
        trade_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": round(self.lot_size, 2),
            "type": self.order_type,
            "deviation": self.deviation_trade,
            "magic": self.magic_number,
            "comment": "",
            "type_time": self.symbol_info.order_gtc_mode,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        # If the order type is Buy, calculate the price, stop loss, and take profit
        if self.order_type == 0:  # Buy
            price = self.symbol_info.ask
            sl = round(price - self.stop_loss, self.symbol_info.digits)
            tp = round(price + self.take_profit, self.symbol_info.digits)
        # If the order type is Sell, calculate the price, stop loss, and take profit
        elif self.order_type == 1:  # Sell
            price = self.symbol_info.bid
            sl = round(price + self.stop_loss, self.symbol_info.digits)
            tp = round(price - self.take_profit, self.symbol_info.digits)
        # Update the trade request with the calculated price, stop loss, and take profit
        trade_request.update({"price": price, "sl": sl, "tp": tp})
        return trade_request

    def _checker_request(self, request: dict, send_output_on_retcode_done: bool = True):
        """
        Check if the trade request is valid
        """
        check_result = mt5.order_check(self._build_request())

        # If the trade request is not valid, print an error message and stop the thread
        if check_result.retcode == mt5.TRADE_RETCODE_DONE or check_result.retcode == 0:
            if send_output_on_retcode_done:
                output(
                    f"Order can be send it, {check_result.retcode}. {mt5.last_error()}",
                    "t",
                )
            else:
                pprint(
                    f"Order can be send it, {check_result.retcode}. {mt5.last_error()}"
                )
        else:
            output(
                f"Error at order_check, retcode={check_result.retcode}. {mt5.last_error()}",
                "e",
            )
            self.running = False

    def _operation_module(self):
        """
        Checks if a trade can be placed based on the section time and if no position is currently open.
        If conditions are met, it prepares a trade request.
        """
        # Check if the section time state is True, no position is currently open, and it's the first trade
        if (
            self.section_time_state is True
            and self.section_time_no_position_flag is True
            and self.first_trade_flag is True
        ):
            self._checker_request(self._build_request(), False)
            # Send the trade request
            self.result = mt5.order_send(self._build_request())

            # If the trade request was not successful, print an error message
            if self.result.retcode != mt5.TRADE_RETCODE_DONE:
                output(
                    f"Error at order_send, retcode={self.result.retcode}. {mt5.last_error()}",
                    "e",
                )
            else:
                # If the trade request was successful, print the result and update the first trade flag and running value
                output(f"Position {self.result.order} done", "t")
                output_dict_request(self.result._asdict())

            # Update the first trade flag and running value
            self.first_trade_flag = False
            self.running = False

    def _OnInit(self):
        """
        Called when the trading thread is initialized.
        Sets up the trading parameters and verifies the terminal information.
        """
        self.deviation_trade = int(self.inputs["deviation_trade"])
        self.lot_size = float(self.inputs["lot_size"])
        self.magic_number = int(self.inputs["magic_number"])
        self.order_type = int(self.inputs["select_type"])
        self.stop_loss = float(self.inputs["stop_loss"])
        self.take_profit = float(self.inputs["take_profit"])

        self.section_time_oninit(self.inputs)

        output(
            f"Section Time \n    {self.local_start_hour}:{self.local_start_min}:{self.local_start_sec} to {self.local_end_hour}:{self.local_end_min}:{self.local_end_sec}",
            "s",
        )

        self.terminal_info = mt5.terminal_info()

        output(f"Deploy in {self.terminal_info.name} Terminal", "t")

        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        output("OnInit {}".format(time.strftime("%H:%M:%S", time_broker)), "t")

        self._checker_request(self._build_request(), True)

    def _OnTick(self):
        """
        Called during the trading thread.
        Checks the current time and verifies if a trade can be placed based on the section time.
        """
        if self.required_initializer() is False:
            return

        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        self.section_time_ontick(time_broker)

        self.section_time_verify_no_position_flag(self.symbol)

        output(
            "Time:{}    SectionTimeState:{}    NoPositionFlag:{}    FirstPositionFlag:{}".format(
                time.strftime("%H:%M:%S", time_broker),
                str(self.section_time_state),
                str(self.section_time_no_position_flag),
                str(self.first_trade_flag),
            ),
            "t",
        )

        self._operation_module()

    def _OnDeinit(self):
        """
        This method is called when the trading thread is deinitialized.
        """
        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        output("OnDeinit {}".format(time.strftime("%H:%M:%S", time_broker)), "s")

        self.first_trade_flag = True

    def _method(self):
        """
        This method runs the trading thread. It calls OnInit,
        then enters a loop where it calls OnTrade every second
        as long as the thread is running.
        """
        self.required_initializer()

        self._OnInit()
        time.sleep(1)
        while self.running:
            self._OnTick()
            time.sleep(1)
        else:
            self._OnDeinit()

    def start(self, inputs_dict=None, symbol: str = "US30"):
        """
        This method starts the trading thread
        if it is not already running. It sets the running value
        to True and starts a new thread targeting the method function.
        """
        # Try to initialize the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            output("Account not logged", "w")
            self.stop()  # Stop the trading thread if the initialization fails
            return

        info_symbol = mt5.symbol_info(symbol)

        self.symbol = info_symbol.name
        # Check if the symbol is available
        if info_symbol is None:
            output(f"Symbol {self.symbol} not allowed, Deploy failed", "e")
            return
        else:
            # If the symbol is unavailable in MarketWatch, add it
            if not info_symbol.visible:
                output(f"{self.symbol}, is not visible, trying to switch ON", "e")
                if not mt5.symbol_select(self.symbol, True):
                    mt5.shutdown()

            info_terminal = mt5.terminal_info()

            if not info_terminal.trade_allowed:
                output(
                    "Algo Traiding is Disable. Please, Turn On and Redeploy Bot", "e"
                )
                mt5.shutdown()
                return

            if info_terminal.tradeapi_disabled:
                output("Sorry, Broker is blocked connection to MT5 API", "e")
                mt5.shutdown()
                return

        # Check if there's already a thread running
        if self.thread is not None:
            pprint("Already there is a thread running")
        else:
            # Show the "Undeploy" button and hide the "Deploy" button
            show_item(dt.set_input_button_undeploy["tag"])
            enable_item(dt.set_input_button_undeploy["tag"])
            hide_item(dt.set_input_button_deploy["tag"])
            disable_item(dt.set_input_button_deploy["tag"])

            # If there are any inputs, set them
            if inputs_dict is not None or not isinstance(inputs_dict, dict):
                self.inputs = inputs_dict

            # Set the running value to True and start the trading thread
            self.running = True
            self.thread = Thread(target=self._method)
            self.thread.start()

    def stop(self):
        """
        This method stops the trading thread if it is running.
        It sets the running value to False, joins the thread,
        and sets the thread to None.
        """
        # Check if there's a thread running
        if self.thread is None:
            pprint("There isn't a thread running")
        else:
            # Show the "Deploy" button and hide the "Undeploy" button
            hide_item(dt.set_input_button_undeploy["tag"])
            disable_item(dt.set_input_button_undeploy["tag"])
            show_item(dt.set_input_button_deploy["tag"])
            enable_item(dt.set_input_button_deploy["tag"])

            # Stop the trading thread
            self.running = False
            self.thread.join()
            self.thread = None
            # Shut down the MetaTrader 5 terminal
            mt5.shutdown()
            save_csv_when_stop()
