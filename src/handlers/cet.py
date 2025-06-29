import re
from datetime import timedelta

from ..colorize import Color
from .compatibility import CompatibleAll
from .handler import Handler


class Cet(CompatibleAll, Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        # dashes in session id when establisher is CReplicationModel
        r'(?:\[SPAM \d+\])?\[(?:Notice|Error)\] <C?ContextEstablisherTask(Finished|LongWait|Failed)> establisher="\w+" message="[\w\s]+" taskname="([\w\.]+)" state=eCVS_(\w+)\((\d+)\) status="[\w\s\d\.]+" runningTime=(\d+\.\d+) numRuns=\d+ map="megamap" gamerules="(.*?)"'
    )

    def format(self, data) -> tuple[int, str]:
        step_num = data[4]
        if data[1] == "Finished":
            which = (
                (
                    Color.GREEN("Complete")
                    if step_num == str(self.state.cet_steps)
                    else "Complete"
                ),
                "in",
            )
        elif data[1] == "LongWait":
            which = (Color.YELLOW("Busy".rjust(8)), "for")
        else:  # ContextEstablisherTaskFailed
            which = (Color.RED("Failed".rjust(8)), "after")

        taskname = data[2]
        step = data[3]

        running_time = round(float(data[5]))
        if running_time > 300:
            running_time_color = "RED"
        elif running_time > 150:
            running_time_color = "YELLOW"
        else:
            running_time_color = "CYAN"
        running_time_str = Color[running_time_color](
            str(timedelta(seconds=running_time))
        )

        lc = 0
        # Replace the previous line if it was a CET, verbose is disabled,
        # and previous CET took less than 5s
        if (
            not self.state.args.verbose
            and self.state.prev_event
            and self.state.prev_event[1] == self.name()
            and float(self.state.prev_event[2][5]) < 5
        ):
            lc = -1
        return (
            lc,
            f"{which[0]}: {step_num.rjust(2)}/{self.state.cet_steps} {Color.CYAN(step)}:{Color.CYAN(taskname)} {which[1]} {running_time_str}",
        )

    def after(self, data):
        # Remove CET once game is loaded.
        # Restored by EndSession.after
        if (
            data[3] == "InGame"
            and data[2] == "InitView.ClientPlayer"
            and data[6] == "SC_Default"  # is SC_Frontend when loading back into menu
        ):
            self.state.handlers.pop(self.name())
