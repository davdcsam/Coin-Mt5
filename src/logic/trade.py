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
from src.interface.terminal_output import output
from src.logic.system_data import InternalData

data = InternalData()


class SectionTime:
    def __init__(self) -> None:
        self.section_time_state = False
        self.section_time_no_position_flag = False
        self.total_positions_magic_symbol = None
        self.positions_symbols_magic = {}

    def section_time_oninit(self, inputs: dict):
        self.local_start_hour = int(inputs["start_hour"])
        self.local_start_min = int(inputs["start_min"])
        self.local_start_sec = int(inputs["start_sec"])
        self.local_end_hour = int(inputs["end_hour"])
        self.local_end_min = int(inputs["end_min"])
        self.local_end_sec = int(inputs["end_sec"])
        self.magic_number = int(inputs["magic_number"])

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
        if self.section_time_no_position_flag:
            # pprint(
            #     "section_time_first_time_flag already is {}".format(
            #         self.section_time_no_position_flag
            #     )
            # )
            return

        positions_symbol = mt5.positions_get(symbol=symbol)
        if len(positions_symbol) == 0:
            pprint(f"No positions in {symbol}")
            self.section_time_no_position_flag = True
        else:
            self.df_positions_symbol = pd.DataFrame(
                list(positions_symbol),
                columns=positions_symbol[0]._asdict().keys(),
            )
            df_positions_symbol_magic_zero = self.df_positions_symbol[
                self.df_positions_symbol["magic"] == self.magic_number
            ]

            if len(df_positions_symbol_magic_zero) == 0:
                self.section_time_no_position_flag = True
            else:
                self.section_time_no_position_flag = False


class Trade(SectionTime):
    """
    The Trade class is designed to handle trading processes.
    It uses multiprocessing to run trading methods in a separate process.
    """

    def __init__(self) -> None:
        """
        Initializes the Trade class with a process set to None
        and a multiprocessing Value indicating whether the process is running.
        """
        super().__init__()
        self.process = None
        self.running = Value("b", False)
        self.queue = Queue()
        self.symbol = "EURUSD"
        self.order_types_dict = {"Buy": mt5.ORDER_TYPE_BUY, "Sell": mt5.ORDER_TYPE_SELL}
        self.first_trade_flag = True

    def required_initializer(self) -> None:
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            self.queue.put((f"Initialize failed, error code: {mt5.last_error()}", "e"))
            self.stop()
            quit()

        # Attempt to enable the display of the EURUSD in MarketWatch
        selected = mt5.symbol_select(self.symbol, True)
        if not selected:
            self.queue.put((f"Failed to select {self.symbol}"))
            self.stop()
            quit()

        self.symbol_info = mt5.symbol_info(self.symbol)

        # pprint(self.symbol_info._asdict())

        if self.symbol_info is None:
            self.queue.put((f"{self.symbol} not found, cannot check orders", "e"))
            self.stop()
            quit()

    def _OnInit(self):
        """
        This method is called when the trading process is initialized.
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
            ("OnInit {}".format(time.strftime("%H:%M:%S", time_broker)), "s")
        )

    def _OnTick(self):
        """
        This method is called during the trading process.
        """
        self.required_initializer()

        time_broker = time.gmtime(mt5.symbol_info_tick(self.symbol).time)

        self.section_time_ontick(time_broker)

        self.section_time_verify_no_position_flag(self.symbol)

        self.queue.put(
            (
                "Time:{} FST:{} FTF:{}".format(
                    time.strftime("%H:%M:%S", time_broker),
                    str(self.section_time_state),
                    str(self.section_time_no_position_flag),
                ),
                "s",
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
        if (
            self.section_time_state is True
            and self.section_time_no_position_flag is True
            and self.first_trade_flag is True
        ):
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
            if self.order_type == 0:  # Buy
                price = self.symbol_info.ask
                sl = price - self.stop_loss
                tp = price + self.take_profit
            elif self.order_type == 1:  # Sell
                price = self.symbol_info.bid
                sl = price + self.stop_loss
                tp = price - self.take_profit
            self.trade_request.update({"price": price, "sl": sl, "tp": tp})

            check_result = mt5.order_check(self.trade_request)

            pprint(self.trade_request)

            if check_result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Error at order_check, retcode={}".format(check_result.retcode))
                self.running.value = False
            else:
                print("Order can be send it, ", check_result)

            self.result = mt5.order_send(self.trade_request)

            if self.result.retcode != mt5.TRADE_RETCODE_DONE:
                self.queue.put(
                    ("Error en order_send, retcode={}".format(self.result.retcode), "e")
                )
            else:
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

        # Check if the symbol is available
        if mt5.symbol_info(symbol) is None:
            output(f"Symbol {symbol} not allowed, Deploy failed", "e")
            return
        else:
            s_info = mt5.symbol_info(symbol)
            self.symbol = s_info.name
            # If the symbol is unavailable in MarketWatch, add it
            if not s_info.visible:
                output(f"{self.symbol}, is not visible, trying to switch ON", "e")
                if not mt5.symbol_select(self.symbol, True):
                    mt5.shutdown()
                    quit()

        # Check if there's already a process running
        if self.process is not None:
            pprint("Already there is a process running")
        else:
            # Show the "Undeploy" button and hide the "Deploy" button
            show_item(data.set_input_button_undeploy["tag"])
            enable_item(data.set_input_button_undeploy["tag"])
            hide_item(data.set_input_button_deploy["tag"])
            disable_item(data.set_input_button_deploy["tag"])

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
            hide_item(data.set_input_button_undeploy["tag"])
            disable_item(data.set_input_button_undeploy["tag"])
            show_item(data.set_input_button_deploy["tag"])
            enable_item(data.set_input_button_deploy["tag"])

            # Stop the trading process
            self.running.value = False
            self.process.join()
            self.process = None
            # Shut down the MetaTrader 5 terminal
            mt5.shutdown()
