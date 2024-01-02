import os
from termcolor import colored

# hehe

class printf:
    """
    `@!{text}$&` => Bold text \n
    `@?{text}$&` => Italic text \n
    `@~{text}$&` => Dim text \n
    `@_{text}$&` => Underlined text \n


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

    def full_line(*args, **kwargs) -> None:
        terminal_width: int = os.get_terminal_size().columns
        joiner = " "
        if kwargs.get("sep"):
            joiner = kwargs.get("sep")

        content = joiner.join(args)

        printf(f'{printf.__filter(content)}{" "*(terminal_width - len(printf.__rm_filter(content)))}', **kwargs)

    def full() -> None:
        for i in range(os.get_terminal_size().lines - 1):
            printf.full_line(end="\n")

    def endl(times: int = 1):
        print("\n" * times, end="")

    def title(content: str, line_char: chr = "─") -> None:
        width: int = os.get_terminal_size().columns
        mid_text: str = f" {content} "
        side_width: int = int((width - len(printf.__rm_filter(mid_text))) / 2)

        if len(line_char) != 1:
            raise ValueError("line char is not a char")

        sep_text = line_char * side_width
        printf.endl(5)
        printf(f"{sep_text}{mid_text}{sep_text}")
        printf.endl()

    def clear_screen() -> None:
        # Clear the terminal screen using ANSI escape code
        os.system("cls" if os.name == "nt" else "clear")