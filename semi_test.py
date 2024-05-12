
import src.zenyx as zenyx
import sys
import tests.databank as db


from result import *

def unit(u: str) -> float:
    """
    ## Units
    x   - pixel\n
    h   - screen height\n
    w   - screen width\n
    u   - 16px \n

    ## Example
    ```
    el(
        style=style(
            x="12u",
            y="14w"
        )
    )
    ```
    """

    # num_res = float(u[:-1])

    # if num_res.is_err():
    #     return 0

    num: float = float(u[:-1])

    match u[-1]:
        case "x":
            return num

        case "h":
            return 1600 * (num / 100)

        case "w":
            return 1600 * (num / 100)

        case "u":
            return num * 16

def err():
    raise Exception("asdasd")

def test_one():
    print(unit('50x'))

    x = zenyx.std.attempt(err, [])

    if x.is_err():
        print(x.err())


test_one()