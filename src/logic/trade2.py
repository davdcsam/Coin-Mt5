# Standard
from multiprocessing import Value, Process, Queue
from multiprocessing.reduction import DupHandle
import time

# Third Party
import MetaTrader5 as mt5

import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import set_item_callback, set_item_label

# Owner

from src.interface.terminal_output import output
from src.logic.system_data import InternalData

data = InternalData()

class Trade:
    """
    The Trade class is designed to handle trading processes.
    It uses multiprocessing to run trading methods in a separate process.
    """

    def __init__(self) -> None:
        """
        Initializes the Trade class with a process set to None
        and a multiprocessing Value indicating whether the process is running.
        """
        self.process = None
        self.running = Value("b", False)
        self.queue = Queue()
        self.symbol = "EURUSD"

    def required_initializer(self):
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        # Attempt to enable the display of the EURUSD in MarketWatch
        selected = mt5.symbol_select(self.symbol, True)
        if not selected:
            print(f"Failed to select {self.symbol}")
            mt5.shutdown()
            quit()

    def OnInit(self):
        """
        This method is called when the trading process is initialized.
        It prints the current time.
        """
        self.required_initializer()
        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick(self.symbol)

        time_broker = time.gmtime(symbol_info_tick.time)

        time_broker = time.strftime("%H:%M:%S", time_broker)

        self.queue.put(("OnInit {}".format(time_broker), "s"))

    def OnTrade(self):
        """
        This method is called during the trading process.
        It prints the current time.
        """
        self.required_initializer()

        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick(self.symbol)

        time_broker = time.gmtime(symbol_info_tick.time)

        time_broker = time.strftime("%H:%M:%S", time_broker)

        self.queue.put(("{}".format(time_broker), "s"))

    def OnDeinit(self):
        """
        This method is called when the trading process is deinitialized.
        It prints the current time.
        """
        self.required_initializer()

        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick(self.symbol)

        time_broker = time.gmtime(symbol_info_tick.time)

        time_broker = time.strftime("%H:%M:%S", time_broker)

        self.queue.put(("OnDeinit {}".format(time_broker), "s"))

    def method(self):
        """
        This method runs the trading process. It calls OnInit,
        then enters a loop where it calls OnTrade every second
        as long as the process is running, and finally calls
        OnDeinit when the process stops.
        """
        self.OnInit()
        time.sleep(1)
        while self.running.value:
            self.OnTrade()
            time.sleep(1)

    def start(self, inputs_dict=None, symbol=None):
        """
        This method starts the trading process
        if it is not already running. It sets the running value
        to True and starts a new process targeting the method function.
        """
        # Try to initialize the MetaTrader 5 terminal
        if not mt5.initialize(timeout=1000):
            output("Account not logged", "w")
            self.stop()  # Stop the trading process if the initialization fails
        else:
            # Check if there's already a process running
            if self.process is not None:
                print("Ya se está ejecutando un proceso")
            else:
                # Show the "Undeploy" button and hide the "Deploy" button
                dpg.show_item(data.set_input_button_undeploy["tag"])
                dpg.enable_item(data.set_input_button_undeploy["tag"])
                dpg.hide_item(data.set_input_button_deploy["tag"])
                dpg.disable_item(data.set_input_button_deploy["tag"])

                # If there are any inputs, set them
                if inputs_dict is not None:
                    self.inputs = inputs_dict
                    print(self.inputs)

                # Set the running value to True and start the trading process
                self.running.value = True
                self.process = Process(target=self.method)
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
            print("No hay ningún proceso en ejecución")
        else:
            # Show the "Deploy" button and hide the "Undeploy" button
            dpg.hide_item(data.set_input_button_undeploy["tag"])
            dpg.disable_item(data.set_input_button_undeploy["tag"])
            dpg.show_item(data.set_input_button_deploy["tag"])
            dpg.enable_item(data.set_input_button_deploy["tag"])

            # Call the OnDeinit method and stop the trading process
            self.OnDeinit()
            self.running.value = False
            self.process.join()
            self.process = None
            mt5.shutdown()  # Shut down the MetaTrader 5 terminal


