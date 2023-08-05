from je_editor.ui.ui_utils.editor_content.content_save import save_content_and_quit


def close_event(check_current_file, tkinter_window, exec_manager):
    """
    :param exec_manager:
    :param check_current_file: check have current file? if have; save and quit else only quit
    :param tkinter_window: the tkinter window will close
    :return: no return value
    """
    if check_current_file is not None:
        save_content_and_quit(check_current_file)
    exec_manager.exit_program()
    tkinter_window.destroy()
