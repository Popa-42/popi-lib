import os
import sys

import colorama

escape_code_dict: dict = {
    "": "",
    "<reset>": "\033[0m",
    "<b>": "\033[1m",
    "<i>": "\033[3m",
    "<u>": "\033[4m",
    "<black>": "\033[30m",
    "<red>": "\033[31m",
    "<green>": "\033[32m",
    "<yellow>": "\033[33m",
    "<blue>": "\033[34m",
    "<magenta>": "\033[35m",
    "<cyan>": "\033[36m",
    "<white>": "\033[37m",
    "<black_bg>": "\033[40m",
    "<red_bg>": "\033[41m",
    "<green_bg>": "\033[42m",
    "<yellow_bg>": "\033[43m",
    "<blue_bg>": "\033[44m",
    "<magenta_bg>": "\033[45m",
    "<cyan_bg>": "\033[46m",
    "<white_bg>": "\033[47m",
    "<bright_black>": "\033[90m",
    "<bright_red>": "\033[91m",
    "<bright_green>": "\033[92m",
    "<bright_yellow>": "\033[93m",
    "<bright_blue>": "\033[94m",
    "<bright_magenta>": "\033[95m",
    "<bright_cyan>": "\033[96m",
    "<bright_white>": "\033[97m",
    "<bright_black_bg>": "\033[100m",
    "<bright_red_bg>": "\033[101m",
    "<bright_green_bg>": "\033[102m",
    "<bright_yellow_bg>": "\033[103m",
    "<bright_blue_bg>": "\033[104m",
    "<bright_magenta_bg>": "\033[105m",
    "<bright_cyan_bg>": "\033[106m",
    "<bright_white_bg>": "\033[107m",
    "<hr>": "",
}


def terminal_supports_colors() -> bool:
    """
    Check if the terminal supports ANSI escape codes.

    :return: True if the terminal supports ANSI escape codes, False otherwise.
    """
    # Initialise colorama
    if os.name == "nt":
        colorama.init()
    # Check if the terminal runs on Windows and supports ANSI escape codes
    if os.name == "nt":
        return sys.stdout.isatty()

    # Check if the terminal runs on Unix and supports ANSI escape codes
    if sys.platform != "win32" and sys.stdout.isatty():
        return True
    return False


def text2escape(html: str) -> str:
    for key, value in escape_code_dict.items():
        if terminal_supports_colors():
            html = html.replace(key, value)
        else:
            html = html.replace(key, "")
    return html
