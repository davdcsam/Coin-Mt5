# Standard
from multiprocessing import Value, Process, Queue
import time
from pprint import pprint

# Third Party
import MetaTrader5 as mt5
import pandas as pd

# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import show_item, hide_item, enable_item, disable_item

# Owner
from src.logic.print_output import output, save_csv_when_stop
from src.logic.system_data import InternalData

"""
Dont implement dt has a atr into Trade class, 'cuase when
process _method start take dt has a Dict incallable
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
        # Checking if the section_time_no_position_flag is already set
        if self.section_time_no_position_flag:
            # pprint(
            #     "section_time_first_time_flag already is {}".format(
            #         self.section_time_no_position_flag
            #     )
            # )
            return

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
    The Trade class is a subclass of SectionTime, designed to manage trading processes in a separate process using multiprocessing.
    It handles the initialization, execution, and deinitialization of trades, and provides real-time updates on the trading process.
    """

    def __init__(self) -> None:
        super().__init__()
        self.process = None
        self.running = Value("b", False)
        self.queue = Queue()
        self.symbol = "EURUSD"
        self.order_types_dict = {"Buy": mt5.ORDER_TYPE_BUY, "Sell": mt5.ORDER_TYPE_SELL}
        self.first_trade_flag = True

    def required_initializer(self) -> None:
        """
        Establishes connection to the MetaTrader 5 terminal and enables the display of the EURUSD in MarketWatch.
        If any of these operations fail, it stops the process and quits.
        """
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            self.queue.put((f"Initialize failed, error code: {mt5.last_error()}", "e"))
            self.stop()
            quit()

        # Attempt to enable the display of the self.symbol in MarketWatch
        selected = mt5.symbol_select(self.symbol, True)
        if not selected:
            self.queue.put((f"Failed to select {self.symbol}"))
            self.stop()
            quit()

        self.symbol_info = mt5.symbol_info(self.symbol)

        if self.symbol_info is None:
            self.queue.put((f"{self.symbol} not found, cannot check orders", "e"))
            self.stop()
            quit()

        info_terminal = mt5.terminal_info()

        if not info_terminal.trade_allowed:
            self.queue.put(
                ("Algo Traiding is Disable. Please, Turn On", "e")
            )
            return False

        if info_terminal.tradeapi_disabled:
            self.queue.put(("Sorry, Broker blocked connection to MT5 API", "e"))
            return False

        return True

    def _OnInit(self):
        """
        Called when the trading process is initialized.
        Sets up the trading parameters and verifies the terminal information.
        """
        self.deviation_trade = int(self.inputs["deviation_trade"])
        self.lot_size = float(self.inputs["lot_size"])
        self.magic_number = int(self.inputs["magic_number"])
        self.order_type = int(self.inputs["select_type"])
        self.stop_loss = float(self.inputs["stop_loss"])
        self.take_profit = float(self.inputs["take_profit"])

        self.section_time_oninit(self.inputs)

        self.queue.put(
            (
                f"Section Time \n    {self.local_start_hour}:{self.local_start_min}:{self.local_start_sec} to {self.local_end_hour}:{self.local_end_min}:{self.local_end_sec}",
                "s",
            )
        )

        self.terminal_info = mt5.terminal_info()

        self.queue.put((f"Deploy in {self.terminal_info.name} Terminal", "t"))

        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        self.queue.put(
            ("OnInit {}".format(time.strftime("%H:%M:%S", time_broker)), "t")
        )

    def _OnTick(self):
        """
        Called during the trading process.
        Checks the current time and verifies if a trade can be placed based on the section time.
        """
        if self.required_initializer() is False:
            return

        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        self.section_time_ontick(time_broker)

        self.section_time_verify_no_position_flag(self.symbol)

        self.queue.put(
            (
                "Time:{}    SectionTimeState:{}    NoPositionFlag:{}".format(
                    time.strftime("%H:%M:%S", time_broker),
                    str(self.section_time_state),
                    str(self.section_time_no_position_flag),
                ),
                "t",
            )
        )

        self._operation_module()

    def _OnDeinit(self):
        """
        This method is called when the trading process is deinitialized.
        """
        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        self.queue.put(
            ("OnDeinit {}".format(time.strftime("%H:%M:%S", time_broker)), "s")
        )

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
            # Prepare a trade request with the necessary parameters
            self.trade_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": self.lot_size,
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
                sl = price - self.stop_loss
                tp = price + self.take_profit
            # If the order type is Sell, calculate the price, stop loss, and take profit
            elif self.order_type == 1:  # Sell
                price = self.symbol_info.bid
                sl = price + self.stop_loss
                tp = price - self.take_profit
            # Update the trade request with the calculated price, stop loss, and take profit
            self.trade_request.update({"price": price, "sl": sl, "tp": tp})

            # Check if the trade request is valid
            check_result = mt5.order_check(self.trade_request)

            # Print the trade request for debugging purposes
            pprint(self.trade_request)

            # If the trade request is not valid, print an error message and stop the process
            if check_result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Error at order_check, retcode={}".format(check_result.retcode))
                self.running.value = False
            else:
                print("Order can be send it, ", check_result)

            # Send the trade request
            self.result = mt5.order_send(self.trade_request)

            # If the trade request was not successful, print an error message
            if self.result.retcode != mt5.TRADE_RETCODE_DONE:
                self.queue.put(
                    ("Error en order_send, retcode={}".format(self.result.retcode), "e")
                )
            else:
                # If the trade request was successful, print the result and update the first trade flag and running value
                result_dict = self.result._asdict()
                self.queue.put((f"Position {self.result.order} done", "t"))
                for field in result_dict.keys():
                    print("   {}={}".format(field, result_dict[field]))
                    # If this is a trading request structure, display it element by element as well
                    if field == "request":
                        trade_request_dict = result_dict[field]._asdict()
                        for trade_req_filed in trade_request_dict:
                            self.queue.put(
                                (
                                    "         Result: {}={}".format(
                                        trade_req_filed,
                                        trade_request_dict[trade_req_filed],
                                    ),
                                    "t",
                                )
                            )

            # Update the first trade flag and running value
            self.first_trade_flag = False
            self.running.value = False

    def _method(self):
        """
        This method runs the trading process. It calls OnInit,
        then enters a loop where it calls OnTrade every second
        as long as the process is running.
        """
        self.required_initializer()

        self._OnInit()
        time.sleep(1)
        while self.running.value:
            self._OnTick()
            time.sleep(1)
        else:
            self._OnDeinit()

    def start(self, inputs_dict=None, symbol: str = "US30"):
        """
        This method starts the trading process
        if it is not already running. It sets the running value
        to True and starts a new process targeting the method function.
        """
        # Try to initialize the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            output("Account not logged", "w")
            self.stop()  # Stop the trading process if the initialization fails
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

        # Check if there's already a process running
        if self.process is not None:
            pprint("Already there is a process running")
        else:
            # Show the "Undeploy" button and hide the "Deploy" button
            show_item(dt.set_input_button_undeploy["tag"])
            enable_item(dt.set_input_button_undeploy["tag"])
            hide_item(dt.set_input_button_deploy["tag"])
            disable_item(dt.set_input_button_deploy["tag"])

            # If there are any inputs, set them
            if inputs_dict is not None or not isinstance(inputs_dict, dict):
                self.inputs = inputs_dict
                # pprint(self.inputs)

            # Set the running value to True and start the trading process
            self.running.value = True
            self.process = Process(target=self._method)
            self.process.start()

            # Process any messages in the queue
            while self.queue is not None:
                message_queue = self.queue.get()
                output(message_queue[0], message_queue[1])

    def stop(self):
        """
        This method stops the trading process if it is running.
        It sets the running value to False, joins the process,
        and sets the process to None.
        """
        # Check if there's a process running
        if self.process is None:
            pprint("There isn't a procces running")
        else:
            # Show the "Deploy" button and hide the "Undeploy" button
            hide_item(dt.set_input_button_undeploy["tag"])
            disable_item(dt.set_input_button_undeploy["tag"])
            show_item(dt.set_input_button_deploy["tag"])
            enable_item(dt.set_input_button_deploy["tag"])

            # Stop the trading process
            self.running.value = False
            self.process.join()
            self.process = None
            # Shut down the MetaTrader 5 terminal
            mt5.shutdown()
            save_csv_when_stop()
