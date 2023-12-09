# Standard
import sys
from os import getcwd, path, remove

# Third
from dearpygui.dearpygui import (
    add_window,
    configure_app,
    create_context,
    create_viewport,
    destroy_context,
    get_callback_queue,
    is_dearpygui_running,
    render_dearpygui_frame,
    run_callbacks,
    set_exit_callback,
    set_primary_window,
    set_start_callback,
    setup_dearpygui,
    show_viewport,
)

# Owner
from src.interface.menu_bar import MenuBar
from src.interface.set_font import Fonts
from src.interface.set_input import SetInput
from src.interface.terminal_output import TerminalOutput
from src.logic.print_output import save_csv_when_stop
from src.logic.system_data import InternalData


def start_callback(sender, app_data):
    set_input_instance.load_last_inputs(sender=sender, app_data=app_data)


def exit_callback(sender, app_data):
    set_input_instance.save_last_inputs(sender=sender, app_data=app_data)
    dt.save_to_json_files()
    dt.save_to_unit_json_file()
    save_csv_when_stop()


def main():
    global dt, set_input_instance
    # Creating a context for DearPyGUI
    create_context()

    # Configuring the application to manage callbacks manually
    configure_app(manual_callback_management=True)

    icon_small = f"{getcwd()}/assets/coin.ico"
    icon_large = f"{getcwd()}/assets/coin.png"
    # Creating a viewport for the application
    create_viewport(
        title="Coin",
        width=1030,
        height=780,
        resizable=True,
        decorated=True,
        small_icon=icon_small,
        large_icon=icon_large,
    )

    # Setting up DearPyGUI
    setup_dearpygui()

    # Showing the viewport
    show_viewport()

    # Creating an instance of the InternalData class
    dt = InternalData()

    # Adding a window to the application
    main_window = add_window(
        label=dt.main_window["label"],
        tag=dt.main_window["tag"],
    )

    """
    Creating instances of the MenuBar, Fonts,
    SetInput, and TerminalOutput classes.
    """
    menu_bar_instance = MenuBar()
    fonts_instance = Fonts()
    set_input_instance = SetInput(
        tag=dt.set_input_window["tag"],
        parent=main_window,
        width=400,
        pos=(10, 20),
    )
    terminal_output_instance = TerminalOutput(
        tag=dt.terminal_output_window["tag"],
        parent=main_window,
        pos=(400, 20),
    )

    """
    Setting the font, adding a menu bar,
    and adding the input and output sections to the window
    """
    menu_bar_instance.add()
    fonts_instance.set_font()
    set_input_instance.add()
    terminal_output_instance.add()

    # Setting the start and exit callbacks for the application
    set_start_callback(start_callback)
    set_exit_callback(exit_callback)

    # Setting the primary window for the application
    set_primary_window(main_window, True)

    # Running the application
    while is_dearpygui_running():
        jobs = get_callback_queue()
        run_callbacks(jobs)
        render_dearpygui_frame()

    # Destroying the context when the application stops running
    destroy_context()


lock_file = f"{getcwd()}/data/lock.lock"

if __name__ == "__main__":
    if path.exists(lock_file):
        print("Ya se está ejecutando una instancia de la aplicación.")
        sys.exit()
    else:
        # Crea el archivo de bloqueo
        open(lock_file, "a").close()
    try:
        # Ejecuta la aplicación
        main()
    finally:
        # Elimina el archivo de bloqueo cuando la aplicación se cierre
        remove(lock_file)
