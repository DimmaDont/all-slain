from enum import IntEnum



def fg(color: 'Color') -> str:
    return f'\x1b[3{color.value}m'

def bg(color: 'Color') -> str:
    return f'\x1b[4{color.value}m'

def color(text: str, color: 'Color') -> str:
    return f'{fg(color)}{text}{Color.RESET}'


class Color(IntEnum):
    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7

    def __call__(self, text):
        return color(text, self)

Color.RESET = f'{bg(Color.BLACK)}{fg(Color.WHITE)}'

# vim: set expandtab ts=4 sw=4
