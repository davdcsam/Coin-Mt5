# Standard
from datetime import datetime
from multiprocessing import Value, Process, Queue
import time

# Third Party
import MetaTrader5 as mt5

# Owner
from src.interface.terminal_output import output


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

    def OnInit(self):
        """
        This method is called when the trading process is initialized.
        It prints the current time.
        """
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        # Attempt to enable the display of the EURUSD in MarketWatch
        selected = mt5.symbol_select("EURUSD", True)
        if not selected:
            print("Failed to select EURUSD")
            mt5.shutdown()
            quit()

        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick("EURUSD")

        time_broker = time.gmtime(symbol_info_tick.time)

        time_broker = time.strftime("%H:%M:%S", time_broker)

        self.queue.put(("OnInit {}".format(time_broker), "s"))

    def OnTrade(self):
        """
        This method is called during the trading process.
        It prints the current time.
        """
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        # Attempt to enable the display of the EURUSD in MarketWatch
        selected = mt5.symbol_select("EURUSD", True)
        if not selected:
            print("Failed to select EURUSD")
            mt5.shutdown()
            quit()

        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick("EURUSD")

        time_broker = time.gmtime(symbol_info_tick.time)

        time_broker = time.strftime("%H:%M:%S", time_broker)

        self.queue.put(("{}".format(time_broker), "s"))

    def OnDeinit(self):
        """
        This method is called when the trading process is deinitialized.
        It prints the current time.
        """
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()

        # Attempt to enable the display of the EURUSD in MarketWatch
        selected = mt5.symbol_select("EURUSD", True)
        if not selected:
            print("Failed to select EURUSD")
            mt5.shutdown()
            quit()

        # display tick field values in the form of a list
        symbol_info_tick = mt5.symbol_info_tick("EURUSD")

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

    def start(self):
        """
        This method starts the trading process
        if it is not already running.It sets the running value
        to True and starts a new process targeting the method function.
        """
        if self.process is not None:
            print("Ya se está ejecutando un proceso")
        else:
            self.running.value = True
            self.process = Process(target=self.method)
            self.process.start()
            while self.queue is not None:
                message_queue = self.queue.get()
                output(message_queue[0], message_queue[1])

    def stop(self):
        """
        This method stops the trading process if it is running.
        It sets the running value to False, joins the process,
        and sets the process to None.
        """
        if self.process is None:
            print("No hay ningún proceso en ejecución")
        else:
            self.OnDeinit()
            self.running.value = False
            self.process.join()
            self.process = None
