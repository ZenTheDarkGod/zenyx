import os
from termcolor import colored

# hehe

class printf:
    """
    '@!{text}$&' => Bold text
    '@?{text}$&' => Italic text
    '@~{text}$&' => Dim text
    '@_{text}$&' => Underlined text


    """

    def __filter(text: str) -> str:
        res = (
            text.replace("@!", "\033[1m")
            .replace("@?", "\033[3m")
            .replace("@~", "\033[2m")
            .replace("@_", "\033[4m")
            .replace("$&", "\033[0m")
        )
        return res

    def __rm_filter(text: str) -> str:
        res = (
            text.replace("@!", "")
            .replace("@?", "")
            .replace("@~", "")
            .replace("@_", "")
            .replace("$&", "")
        )
        return res

    def __init__(self, *args, **kwargs) -> None:
        args_filtered = []
        for arg in args:
            args_filtered.append(
                printf.__filter(arg)
            )

        print(*args_filtered, **kwargs)
        return None

    def full_line(content: str) -> None:
        terminal_width: int = os.get_terminal_size().columns
        print(f'{printf.__filter(content)}{" "*(terminal_width - len(printf.__rm_filter(content)))}')

    def endl(times: int = 1):
        print("\n" * times, end="")

    def title(content: str) -> None:
        width: int = os.get_terminal_size().columns
        mid_text: str = f" {content} "
        side_width: int = int((width - len(printf.__rm_filter(mid_text))) / 2)
        mid_text = printf.__filter(mid_text)

        sep_text = "─" * side_width
        printf.endl(5)
        print(f"{sep_text}{mid_text}{sep_text}")
        printf.endl()

    def clear_screen() -> None:
        # Clear the terminal screen using ANSI escape code
        os.system("cls" if os.name == "nt" else "clear")