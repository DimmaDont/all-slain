import re
from datetime import timedelta

from colorize import Color

from .handler import Handler


class Cet(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        r'<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[Notice\] <(ContextEstablisherTaskFinished|CContextEstablisherTaskLongWait)> establisher="\w+" message="[\w\s]+" taskname="([\w\.]+)" state=eCVS_(\w+)\((\d+)\) status="\w+" runningTime=(\d+\.\d).*'
    )

    def format(self, data) -> str:
        step_num = data[5]
        which = (
            (
                Color.GREEN("Complete") if step_num == "15" else "Complete",
                "in",
            )
            if data[2] == "ContextEstablisherTaskFinished"
            else (Color.YELLOW("Busy".rjust(8)), "for")
        )
        taskname = data[3]
        step = data[4]
        running_time = int(float(data[6]))
        if running_time > 300:
            running_time_color = "RED"
        elif running_time > 150:
            running_time_color = "YELLOW"
        else:
            running_time_color = "CYAN"
        running_time_text = Color[running_time_color](
            str(timedelta(seconds=running_time))
        )
        if self.state.is_prev_line_cet:
            # Move cursor up one line and clear it
            print("\x1b[1A\x1b[2K", end="")
        return f"{which[0]}: {step_num.rjust(2)}/15 {Color.CYAN(step)}:{Color.CYAN(taskname)} {which[1]} {running_time_text}"
