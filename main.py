# Standard

# Third
from dearpygui.dearpygui import (
    add_window,
    add_button,
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
from src.interface.set_font import Fonts
from src.logic.system_data import InternalData


def start_callback(sender, app_data):
    pass


def exit_callback(sender, app_data):
    data.save_to_json_files()
    data.save_to_unit_json_file()


def main():
    global data
    # Creating a context for DearPyGUI
    create_context()

    # Configuring the application to manage callbacks manually
    configure_app(manual_callback_management=True)

    # Creating a viewport for the application
    create_viewport(
        title="3doors",
        width=1030,
        height=780,
        resizable=True,
        decorated=True,
    )

    # Setting up DearPyGUI
    setup_dearpygui()

    # Showing the viewport
    show_viewport()

    # Creating an instance of the InternalData class
    data = InternalData()

    # Adding a window to the application
    main_window = add_window(
        label=data.main_window["label"],
        tag=data.main_window["tag"],
    )

    add_button(label='test', parent=main_window)

    """
    Creating instances of the Fonts, GetTerminal,
    SetInput, and TerminalOutput classes.
    """
    fonts_instance = Fonts()
    # get_terminal_instance = GetTerminal()
    # set_input_instance = SetInput(
    #     tag=data.set_input_window["tag"],
    #     parent=main_window,
    #     width=400,
    #     pos=(10, 20),
    # )
    # terminal_output_instance = TerminalOutput(
    #     tag=data.terminal_output_window["tag"],
    #     parent=main_window,
    #     width=600,
    #     pos=(400, 20),
    # )

    """
    Setting the font, adding a menu bar,
    and adding the input and output sections to the window
    """
    fonts_instance.set_font()
    # get_terminal_instance.add_menu_bar()
    # set_input_instance.add()
    # terminal_output_instance.add()

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


if __name__ == "__main__":
    main()
