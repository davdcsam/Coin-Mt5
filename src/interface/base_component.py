# Third party
# import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import add_child_window

# Owner
from src.logic.system_data import InternalData


class BaseComponent:
    """
    Base class for user interface components.

    Attributes:
        tag (str): Unique identifier for the component.
        parent (str): Identifier of the parent component.
        window (int): ID of the window created for this component.
    """

    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes a new component.

        Args:
            tag (str): Unique identifier for the component.
            parent (str): Identifier of the parent component.
            **kwargs: Additional arguments for the add_child_window function.
        """
        self.dt = InternalData()

        # Store the tag and parent
        self.tag = tag
        self.parent = parent
        # Create a new window for this component
        self.window = add_child_window(
            tag=self.tag,
            label=self.dt.__getattr__(self.tag)["label"],
            parent=self.parent,
            **kwargs
        )

    def add_components(self, tags, add_function, callback=None, **kwargs):
        """
        Adds child components to this component.

        Args:
            tags (list): List of identifiers for the child components.
            add_function (function): Function to add a new component.
            callback (function, optional): Callback function for the component.
            **kwargs: Additional arguments for the add_function.
        """
        # Iterate over the tags
        for tag in tags:
            # If a callback is provided, add a new component with the callback
            if callback:
                add_function(
                    label=self.dt.__getattr__(tag)["label"],
                    tag=self.dt.__getattr__(tag)["tag"],
                    parent=self.window,
                    callback=callback,
                    **kwargs
                )
            else:
                # Otherwise, add a new component without the callback
                add_function(
                    label=self.dt.__getattr__(tag)["label"],
                    tag=self.dt.__getattr__(tag)["tag"],
                    parent=self.window,
                    **kwargs
                )
