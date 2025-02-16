import re
from datetime import timedelta

from colorize import Color

from .handler import Handler


class Cet(Handler):
    header = ("LOAD", Color.WHITE, True)
    pattern = re.compile(
        # dashes in session id when establisher is CReplicationModel
        r'<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).\d{3}Z> \[(?:Notice|Error)\] <C?ContextEstablisherTask(Finished|LongWait|Failed)> establisher="\w+" message="[\w\s]+" taskname="([\w\.]+)" state=eCVS_(\w+)\((\d+)\) status="[\w\s\d\.]+" runningTime=(\d+\.\d+) numRuns=\d+ map="megamap" gamerules="(.*?)" .*'
    )

    def format(self, data) -> str:
        step_num = data[5]
        if data[2] == "Finished":
            which = (
                (
                    Color.GREEN("Complete")
                    if step_num == str(self.state.cet_steps)
                    else "Complete"
                ),
                "in",
            )
        elif data[2] == "LongWait":
            which = (Color.YELLOW("Busy".rjust(8)), "for")
        else:  # ContextEstablisherTaskFailed
            which = (Color.RED("Failed".rjust(8)), "after")

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

        # Replace the previous line if it was a CET and verbose is disabled
        if (
            self.state.prev_event
            and self.state.prev_event[0] == "CET"
            and not self.state.args.verbose
        ):
            # Move cursor up one line and clear it
            print("\x1b[1A\x1b[2K", end="")
        return f"{which[0]}: {step_num.rjust(2)}/{self.state.cet_steps} {Color.CYAN(step)}:{Color.CYAN(taskname)} {which[1]} {running_time_text}"

    def after(self, data):
        # Move CET to end once game is loaded.
        # Moved back to beginning by EndSession.after
        if (
            data[4] == "InGame"
            and data[3] == "InitView.ClientPlayer"
            and data[7] == "SC_Default"  # is SC_Frontend when loading back into menu
        ):
            self.state.handlers["CET"] = self.state.handlers.pop("CET")
