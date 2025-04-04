from handlers.build import HANDLERS
from state import State


def main():
    min_width = max(len(h.header[0]) for h in HANDLERS)

    if State.header_width != min_width:
        print("Minimum header width:", min_width)
        print("Current header width:", State.header_width)

    if State.header_width >= min_width:
        print("OK")


if __name__ == "__main__":
    main()
