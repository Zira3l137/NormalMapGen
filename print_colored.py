from os import name as os_name
from os import system
from sys import stdout

CLEAR = "cls" if os_name == "nt" else "clear"


def print_colored(color: str, *text: str, end: str = "\n", clear: bool = False) -> None:
    """
    Available colors: red, green, yellow, blue
    ------------------------------------------
    When providing multiple arguments for `*text`, they will be joined as is, without any separation.
    """
    if clear:
        system(CLEAR)
    colors: dict[str, str] = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
    }
    reset = "\x1b[0m"
    _ = stdout.write(colors.get(color, "") + "".join(text) + reset + end)


def print_mixed(
    color: str,
    text: str | list[str],
    colored_text: str | list[str],
    end: str = "\n",
    clear: bool = False,
    colored_first: bool = False,
) -> None:
    """
    Available colors: red, green, yellow, blue
    ------------------------------------------
    When providing a list for `text` or `colored_text`, they will be joined as is, without any separation.
    """
    white_text = "".join(text) if isinstance(text, list) else text
    colored_text = (
        "".join(colored_text) if isinstance(colored_text, list) else colored_text
    )
    if colored_first:
        if clear:
            system(CLEAR)
        print_colored(color, colored_text, end="", clear=False)
        stdout.write(white_text + end)
    else:
        stdout.write(white_text)
        print_colored(color, colored_text, end=end, clear=clear)
