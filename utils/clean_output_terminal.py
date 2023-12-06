# Standard
from os import getcwd, path, remove
from glob import glob

# Third

# Owner
from src.interface.terminal_output import csv_file_path


def clean_output_dir(
    exceptions: list = [path.basename(csv_file_path)],
    directory: str = f"{getcwd()}/files/output_terminal/",
):
    """
    This function cleans a specified directory, removing all .csv files
    except those whose names are in the exceptions list.

    Parameters:
    exceptions (list): A list of file names that should not be deleted.
    directory (str): The path of the directory to be cleaned.

    Returns:
    deleted (list): A list of the names of the files that were deleted.
    """

    # Gets a list of all .csv files in the directory
    files = glob(path.join(directory, "*csv"))

    # Initializes a list to store the names of the deleted files
    deleted = []

    # Iterates over each file in the files list
    for file in files:
        # If the file name is not in the exceptions list, it deletes it
        if path.basename(file) not in exceptions:
            # Deletes the file
            remove(file)
            # Adds the file name to the deleted files list
            deleted.append(path.basename(file))

    # Prints the names of the files that were deleted
    print(deleted)

    # Returns the list of the names of the files that were deleted
    return deleted
