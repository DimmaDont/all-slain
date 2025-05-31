<img src="icon/ded.svg" width="100%" height="128">

# all-slain
Star Citizen Game Log Reader

[![GitHub Release](https://img.shields.io/github/v/release/DimmaDont/all-slain)](https://github.com/DimmaDont/all-slain/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/DimmaDont/all-slain/total)](https://github.com/DimmaDont/all-slain/releases)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Docstring style: google](https://img.shields.io/badge/docstring%20style-google-000000.svg)](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)

This console application monitors the Star Citizen `Game.log` file in real-time, reporting player kills, vehicle kills, game loading progress, respawn events, and [more](#supported-events-in-live).

![example screenshot of the program running in windows console](https://github.com/user-attachments/assets/0fa1d08e-776e-449c-b78b-59bf07c5a20c)

## GUI
For a game overlay, check out [all-slain-gui](https://github.com/DimmaDont/all-slain-gui)!

<details>
<summary>Preview</summary>

![screenshot of all-slain-gui](https://github.com/user-attachments/assets/05419d8b-a686-41d2-bced-04ca9384011a)
</details>

## Requirements
* If the log file is not specified, RSI Launcher `2.2.0`+ is required to automatically find it.

## Developers
If you are using this project as part of another project, see [DEVELOPERS.md](DEVELOPERS.md).

## Usage
1. Start the game, and wait until the EasyAntiCheat splash screen closes and the main game window has appeared.
2. Run the program.

The program can also be run with the game log file as the first parameter in a terminal.\
For example: `E:\allslain.exe E:\StarCitizen\PTU\Game.log`

To run the script instead of the exe, see [Running the script](#running-the-script).

> [!TIP]
> Previous log files can be found in the `logbackups` folder.

<details>
<summary><b><code>allslain.exe --help</code></b></summary>

```
usage: allslain.exe [-h] [-d] [-q] [-r [REPLAY]] [-u] [-v] [--version] [file]

all-slain: Star Citizen Game Log Reader
https://github.com/DimmaDont/all-slain

positional arguments:
  file

options:
  -h, --help            show this help message and exit
  -d, --debug
  -q, --quit-on-eof     quit when end of log is reached
  -r, --replay [REPLAY]
                        replays the log as if running live. optionally, specify the maximum number of seconds to wait between each line
  -u, --update          check for updates and exit
  -v, --verbose
  --version             show program's version number and exit
```
</details>

## Game Log Version Compatibility
Compatible with `LIVE` (`4.1.1`).\
Originally developed for `4.0_PREVIEW`.\
Mostly compatible with `3.24.X`.

## Supported Events in LIVE
* Player/NPC deaths[^5]
* Ship/vehicle destruction
* Player respawns/corpse activity
* Game load progress[^1]
* Quit to menu/desktop[^1]
* Incapacitation events[^2]
* Medical bed limb healing[^1]

## Supported Events from Previous Patches
* Inter-system jumps[^1][^8]
* Quantum travel events with destination[^1][^3]
* Quantum travel events[^4][^6]

## Optional Additional Features
* Player organization lookup
* Planespotting[^7]

See the `allslain.conf.toml` config file after first run.\
It can be opened with Notepad, but an editor with syntax highlighting such as [Notepad++](https://notepad-plus-plus.org/) is recommended.

[^1]: Local client only
[^2]: Excludes incaps from combat
[^3]: Only available for `4.0_PREVIEW`
[^4]: Excludes local player
[^5]: Available from `3.24` to `4.0.1`. Since `4.0.2`, only events involving the client player are logged.
[^6]: Only available up to and including `4.0.1`
[^7]: Only available up to and including `4.0.2`. Unavailable since `4.1.0`.
[^8]: Only available up to and including `4.1.0`. Unavailable since `4.1.1`.

## Help Wanted

### Location names and IDs

Locations with missing names will display a red question mark before the ID.

If you find one, please [let us know](https://github.com/Dimmadont/all-slain/issues/new?template=location.yml)!

## Running the script
1. Install [Python](https://www.python.org/downloads/)
2. [Download a copy](https://github.com/DimmaDont/all-slain/archive/refs/heads/master.zip) of the project, and unzip it.
3. Run `run.bat`

## Supported Python Versions
* 3.10+

## Disclaimer
"This is an unofficial Fansite."

Star Citizen intellectual property, content, and trademarks are owned by Cloud Imperium Rights LLC, Cloud Imperium Rights Ltd., and their subsidiaries.
