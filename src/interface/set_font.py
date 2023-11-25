# Standard
# import os
from os import path, getcwd

# Third
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import add_font, bind_font, bind_item_font, font_registry

# Owner


class Fonts:
    """
    Singleton class for managing fonts.

    Attributes:
        _instance (Fonts): The singleton instance of the class.
        fonts (dict): Dictionary to store the created fonts.
    """

    _instance = None

    def __new__(cls):
        """
        Creates a new instance if it does not exist,
        otherwise returns the existing instance.
        """
        if cls._instance is None:
            cls._instance = super(Fonts, cls).__new__(cls)
            cls._instance.fonts = {}  # Initialize the fonts dictionary
        return cls._instance

    def create_fonts(self):
        """
        Creates the fonts and stores them in the fonts dictionary.
        """
        with font_registry():
            self.fonts["opensans_regular_font_20"] = add_font(
                path.join(
                    getcwd(), "assets", "OpenSans", "static", "OpenSans-Regular.ttf"
                ),
                20,
            )
            self.fonts["opensans_semibold_font_30"] = add_font(
                path.join(
                    getcwd(), "assets", "OpenSans", "static", "OpenSans-SemiBold.ttf"
                ),
                24,
            )

    def set_font(self):
        """
        Sets the default font for the application.
        """
        self.create_fonts()
        bind_font(self.fonts["opensans_regular_font_20"])

    def set_font_item(self, tag):
        """
        Sets the font for a specific item.

        Args:
            tag (str): The tag of the item.
        """
        bind_item_font(tag, self.fonts["opensans_semibold_font_30"])

    def set_font_items(self, tags):
        """
        Sets the font for multiple items.

        Args:
            tags (list): A list of tags for the items.
        """
        for tag in tags:
            bind_item_font(tag, self.fonts["opensans_semibold_font_30"])
