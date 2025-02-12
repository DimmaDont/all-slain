from dataclasses import dataclass


@dataclass
class State:
    handlers: dict
    header_width = 9
    is_prev_line_cet: bool = False
