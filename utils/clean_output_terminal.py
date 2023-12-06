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
    files = glob(path.join(directory, "*csv"))

    deleted = []

    for file in files:
        if path.basename(file) not in exceptions:
            remove(file)
            deleted.append(path.basename(file))

    print(deleted)

    return deleted
