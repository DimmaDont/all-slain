<img src="icon/ded.svg" width="100%" height="128">

# all-slain
Star Citizen Game Log Reader

[![GitHub Release](https://img.shields.io/github/v/release/DimmaDont/all-slain)](https://github.com/DimmaDont/all-slain/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/DimmaDont/all-slain/total)](https://github.com/DimmaDont/all-slain/releases)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Docstring style: google](https://img.shields.io/badge/docstring%20style-google-000000.svg)](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)

This program monitors the Star Citizen `Game.log` file in real-time, reporting player kills, vehicle kills, game loading progress, respawn events, and [more](#supported-events).

![example screenshot of the program running in windows console](https://github.com/user-attachments/assets/0fa1d08e-776e-449c-b78b-59bf07c5a20c)

## Requirements
* If the log file is not specified, RSI Launcher `2.2.0` is required to automatically find it.

## Usage
1. Start the game, and wait until the EasyAntiCheat splash screen closes and the main game window has appeared.
2. Run the program.

The program can also be run with the game log file as the first parameter in a terminal.\
For example: `E:\allslain.exe E:\StarCitizen\PTU\Game.log`

> [!TIP]
> Previous log files can be found in the `logbackups` folder.

<details>
<summary><b><code>allslain.exe --help</code></b></summary>

```
usage: allslain.exe [-h] [-d] [-r] [-q] [-u] [-v] [--version] [file]

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  -d, --debug
  -r, --replay          replays the log as if running live
  -q, --quit-on-eof     quit when end of log is reached
  -u, --check-for-updates
                        check for updates and exit
  -v, --verbose
  --version             show program's version number and exit
```
</details>

## Game Log Version Compatibility
Compatible with `LIVE` (`4.0.1`).\
Originally developed for `4.0_PREVIEW`.\
Mostly compatible with `3.24.X`.

## Supported Events
* Player/NPC deaths
* Ship/vehicle destruction
* Player respawns
* Game load progress[^1]
* Quantum travel events[^1][^3], including inter-system jumps[^1]
* Quit to menu/desktop[^1]
* Incapacitation events[^2]

[^1]: Local client only
[^2]: Excludes incaps from combat
[^3]: Only available for `4.0_PREVIEW`

## Fun Fact
* Kills weren't logged until `3.24`

## Known Issues
* Antimalware False Positive\
See [pyinstaller's antivirus issue template](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md).\
Workaround: Install [Python](https://www.python.org/downloads/) manually, download a copy of the repo, install dependencies, and run `allslain.py`.

## Supported Python Versions
* 3.10+

## Disclaimer
"This is an unofficial Fansite."

Star Citizen intellectual property, content, and trademarks are owned by Cloud Imperium Rights LLC, Cloud Imperium Rights Ltd., and their subsidiaries.
