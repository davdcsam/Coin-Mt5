# Standard
from threading import Thread
from os import getcwd


# Third Party
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import (
    add_combo,
    add_text,
    add_input_float,
    add_input_int,
    add_time_picker,
    add_button,
)

# Owner
from src.interface.base_component import BaseComponent
from src.interface.set_font import Fonts
from src.logic.load_save_files import InvalidFormatError, LoadFiles, SaveFiles
from src.logic.system_data import InternalData
from src.logic.trade import Trade


data = InternalData()
fonts_instance = Fonts()


class SetInput(BaseComponent, LoadFiles, SaveFiles):
    """
    Class for setting input fields in a DearPyGUI window.

    Attributes:
        sections (list): List of sections to be added to the window.
        filedailog_filetypes (tuple): File types for
          the file dialog.
        categories (dict): Categories of input fields.
        last_input_filename (str): Path to the last inputs file.
        trade_instance (class 'src.logic.trade.Trade'): Trade Instance
    """

    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes the input fields in a DearPyGUI window.

        Args:
            tag (str): Unique label for the component.
            parent (str): Label of the parent component.
        """
        self.filedailog_filetypes = (("Set Files", "*.set"), ("All files", "*.*"))
        self.categories = {
            "Trade": [
                "select_type",
                "lot_size",
                "stop_loss",
                "take_profit",
                "magic_number",
                "deviation_trade",
            ],
            "Section Time": [
                "section_time_start",
                "section_time_end",
            ],
            "Start Section": [
                "start_hour",
                "start_min",
                "start_sec",
            ],
            "End Section": [
                "end_hour",
                "end_min",
                "end_sec",
            ],
        }
        self.last_input_filename = f"{getcwd()}/data/last_inputs.set"

        self.trade_instance = Trade()

        BaseComponent.__init__(self, tag, parent, **kwargs)
        InvalidFormatError.__init__(self)
        LoadFiles.__init__(
            self, self.categories, self.filedailog_filetypes, self.last_input_filename
        )
        SaveFiles.__init__(
            self, self.categories, self.filedailog_filetypes, self.last_input_filename
        )
        self.sections = [
            ("title", None),
            ("title_data_trade", self.data_trade),
            ("title_section_time", self.section_time),
            (None, self.load_save),
            ("title_bot_manager", self.bot_manager),
        ]

    def add(self):
        """
        Adds sections and a load/save button to the window.
        """
        # Iterate over the sections
        for section, function in self.sections:
            """
            If a sections is diferent to None,
            add a text field to the window for each section.
            And set the title font
            """
            if section is not None:
                add_text(
                    data.__getattr__(f"set_input_text_{section}")["label"],
                    tag=data.__getattr__(f"set_input_text_{section}")["tag"],
                    parent=self.window,
                )
                fonts_instance.set_font_item(
                    data.__getattr__(f"set_input_text_{section}")["tag"]
                )

            """
            If a function is provided for the section,
            call it with the window as the parent
            """
            if function is not None:
                function(parent=self.window)

    def data_trade(self, parent):
        """
        Adds data trade input fields to the window.

        Args:
            parent: The parent widget.
        """
        self.list_order_type = [
            key for key in self.trade_instance.order_types_dict.keys()
        ]
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
            items=["US30", "US100"],
            width=200,
        )

    ###########################################################################

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
            args=(self.get_values(sender, app_data),),
        )
        # Start the new thread
        thread.start()

    ##########################################################################

    #########################################################################
