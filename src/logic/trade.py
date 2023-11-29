# Standard
from multiprocessing import Value, Process, Queue
import time
from pprint import pprint

# Third Party
import MetaTrader5 as mt5

# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import show_item, hide_item, enable_item, disable_item

# Owner

from src.interface.terminal_output import output
from src.logic.system_data import InternalData

data = InternalData()


class SectionTime:
    def __init__(self) -> None:
        self.section_time_state = False

    def section_time_onint(self, inputs: dict = None):
        self.local_start_hour = inputs["start_hour"]
        self.local_start_min = inputs["start_min"]
        self.local_start_sec = inputs["start_sec"]
        self.local_end_hour = inputs["end_hour"]
        self.local_end_min = inputs["end_min"]
        self.local_end_sec = inputs["end_sec"]


class TimeBroker:
    def update_time(self, symbol: str):
        self.symbol_info_tick = mt5.symbol_info_tick(symbol)
        self.time_broker = time.gmtime(self.symbol_info_tick.time)
        self.time_broker = time.strftime("%H:%M:%S", self.time_broker)


class Trade(SectionTime, TimeBroker):
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

        self.terminal_info = mt5.terminal_info()

        self.section_time_onint(self.inputs)

        self.queue.put((f"Section Time \n    {self.local_start_hour}:{self.local_start_min}:{self.local_start_sec} to {self.local_end_hour}:{self.local_end_min}:{self.local_end_sec}", 's'))

        self.queue.put((f"Deploy in {self.terminal_info.name} Terminal", 't'))

        self.update_time(self.symbol)

        self.queue.put(("OnInit {}".format(self.time_broker), "s"))

    def OnTrade(self):
        """
        This method is called during the trading process.
        It prints the current time.
        """
        self.required_initializer()

        self.update_time(self.symbol)

        self.queue.put(("{}".format(self.time_broker), "s"))

    def OnDeinit(self):
        """
        This method is called when the trading process is deinitialized.
        It prints the current time.
        """
        self.required_initializer()

        self.update_time(self.symbol)

        self.queue.put(("OnDeinit {}".format(self.time_broker), "s"))

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
                pprint("Ya se está ejecutando un proceso")
            else:
                # Show the "Undeploy" button and hide the "Deploy" button
                show_item(data.set_input_button_undeploy["tag"])
                enable_item(data.set_input_button_undeploy["tag"])
                hide_item(data.set_input_button_deploy["tag"])
                disable_item(data.set_input_button_deploy["tag"])

                # If there are any inputs, set them
                if inputs_dict is not None:
                    self.inputs = inputs_dict
                    pprint(self.inputs)

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
            pprint("No hay ningún proceso en ejecución")
        else:
            # Show the "Deploy" button and hide the "Undeploy" button
            hide_item(data.set_input_button_undeploy["tag"])
            disable_item(data.set_input_button_undeploy["tag"])
            show_item(data.set_input_button_deploy["tag"])
            enable_item(data.set_input_button_deploy["tag"])

            # Call the OnDeinit method and stop the trading process
            self.OnDeinit()
            self.running.value = False
            self.process.join()
            self.process = None
            mt5.shutdown()  # Shut down the MetaTrader 5 terminal
