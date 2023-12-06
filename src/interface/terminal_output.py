# Standard

# Third Party

# Owner
from src.interface.base_component import BaseComponent
from src.logic.print_output import df, csv_file_path


# Defining a class to manage terminal output in a DearPyGUI window
class TerminalOutput(BaseComponent):
    """
    Class for managing terminal output in a DearPyGUI window.
    """

    # Initializing the terminal output in a DearPyGUI window
    def __init__(self, tag: str, parent: str, **kwargs):
        """
        Initializes the terminal output in a DearPyGUI window.

        Args:
            tag (str): Unique label for the component.
            parent (str): Label of the parent component.
        """
        super().__init__(tag, parent, **kwargs)

    # Adding sections and a load/save button to the window
    def add(self):
        """
        Adds sections and a load/save button to the window.
        Also created a csv file where is saved outputs.
        """
        # Creating a CSV file for the terminal output
        self._create_terminal_output_csv()

    # Creating a CSV file for the terminal output
    def _create_terminal_output_csv(self):
        """
        Creates a CSV file for the terminal output.
        """
        return df.to_csv(csv_file_path, mode="w")
