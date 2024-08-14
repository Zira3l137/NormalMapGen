from sys import stdout


def print_colored(color: str, *text: str, end: str = "\n") -> None:
    """
    Available colors: red, green, yellow, blue
    """
    colors: dict[str, str] = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
    }
    reset = "\x1b[0m"
    _ = stdout.write(colors.get(color, "") + "".join(text) + reset + end)
