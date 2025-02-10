from dataclasses import dataclass


@dataclass
class State:
    header_width = 9
    is_prev_line_cet: bool = False
