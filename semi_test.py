
from src.zenyx import printf, Arguments
import sys

ARGS = Arguments(sys.argv)

def test_one():
    printf.clear_screen()
    printf.full()
    printf.title("@!Bold ass$& / bitches", " ")
    printf.full_line("asd", "asd", sep="-")

    printf(f"{ARGS.normals} | {ARGS.modifiers} | {ARGS.tags}")
    printf(ARGS.tagged("run"))
    printf(ARGS.tagged("build"))
    printf(ARGS.get_modifier_value("mode"))

test_one()