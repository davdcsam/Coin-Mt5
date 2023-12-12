# Standard
from threading import Thread

# Third
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import (
    add_combo,
    add_text,
    add_input_float,
    add_input_int,
    add_time_picker,
    add_button,
    get_value,
)

# Owner
from src.interface.base_component import BaseComponent
from src.interface.set_font import Fonts
from src.logic.load_save_files import LoadFiles, SaveFiles
from src.logic.system_data import InternalData
from src.logic.trade import Trade


class SetInput(BaseComponent, LoadFiles, SaveFiles):
    """
    The SetInput class extends the BaseComponent, LoadFiles, and SaveFiles classes. It represents a user interface component that allows users to set input fields in a DearPyGUI window.

    Attributes:
        fonts_instance (Fonts): An instance of the Fonts class.
        df (InternalData): An instance of the InternalData class.
        trade_instance (Trade): An instance of the Trade class.
        sections (list): A list of tuples, where each tuple contains a section name and a function that adds the section to the window.
    """

    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes a new instance of the SetInput class.

        Args:
            tag (str): A unique identifier for the component.
            parent (str): The identifier of the parent component.
            **kwargs: Additional keyword arguments.
        """
        self.trade_instance = Trade()
        self.fonts_instance = Fonts()
        self.dt = InternalData()
        # Define the sections to be added to the window
        self.sections = [
            ("title", None),
            ("title_data_trade", self.data_trade),
            ("title_section_time", self.section_time),
            (None, self.load_save),
            ("title_bot_manager", self.bot_manager),
        ]

        # Load the symbols
        self.symbols = self.load_symbols()

        # Call the constructors of the parent classes
        BaseComponent.__init__(self, tag, parent, **kwargs)
        LoadFiles.__init__(self, self.trade_instance)
        SaveFiles.__init__(self, self.trade_instance)

    def add(self):
        """
        Adds sections and a load/save button to the window.
        """
        # Iterate over the sections
        for section, function in self.sections:
            # If a section name is provided, add a text field to the window for the section
            if section is not None:
                add_text(
                    self.dt.__getattr__(f"set_input_text_{section}")["label"],
                    tag=self.dt.__getattr__(f"set_input_text_{section}")["tag"],
                    parent=self.window,
                )
                self.fonts_instance.set_font_item(
                    self.dt.__getattr__(f"set_input_text_{section}")["tag"]
                )

            # If a function is provided for the section, call it with the window as the parent
            if function is not None:
                function(parent=self.window)

    def data_trade(self, parent):
        """
        Adds data trade input fields to the window.

        Args:
            parent: The parent widget.
        """
        # Define the list of order types
        self.list_order_type = [
            key for key in self.trade_instance.order_types_dict.keys()
        ]

        # Add components for the data trade input fields
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
            format="%.2f",
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
        # Add components for the time section input fields
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
        # Add components for the load and save input fields
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
        """
        Adds deploy, undeploy and select symbol combo to the window.

        Args:
            parent: The parent widget.
        """
        # Add components for the bot manager input fields
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
        self.add_components(
            ["set_input_select_symbol"],
            add_combo,
            items=self.symbols,
            default_value=self.symbols[0],
            width=200,
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
            args=(
                self.get_values(sender, app_data),
                get_value(self.dt.set_input_select_symbol["tag"]),
            ),
        )
        # Start the new thread
        thread.start()
