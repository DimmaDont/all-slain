<img src="icon/ded.svg" width="100%" height="128">

# all-slain
Star Citizen Game Log Reader

![GitHub Release](https://img.shields.io/github/v/release/DimmaDont/all-slain)
![GitHub Downloads](https://img.shields.io/github/downloads/DimmaDont/all-slain/total)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

This program monitors the Star Citizen `Game.log` file in real-time, reporting player kills, vehicle kills, game loading progress, respawn events, and more.

![example screenshot of the program running in windows console](https://github.com/user-attachments/assets/0fa1d08e-776e-449c-b78b-59bf07c5a20c)

## Usage
1. Start the game, and wait until the EasyAntiCheat splash screen closes and the main game window has appeared.
2. If Star Citizen is installed in the default location, simply run the program.  
3. If Star Citizen is installed elsewhere, move the program into the game folder before running.

The program can also be run with the game log file as the first parameter in a terminal.  
For example: `E:\allslain.exe E:\StarCitizen\PTU\Game.log`

> [!TIP]
> The game moves previous log files into the `logbackups` folder.

## Game Version Compatibility
Developed for `4.0_PREVIEW`.  
Mostly compatible with `LIVE` (3.24.3).

## Fun Fact
* Kills weren't logged until `3.24`

## Known Issues
* Antimalware False Positive  
See [pyinstaller's antivirus issue template](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md).  
Workaround: Install [Python](https://www.python.org/downloads/) manually and run `allslain.py`.

## Supported Python Versions
* 3.11+
* 3.10 with `typing-extensions`

## Disclaimer
"This is an unofficial Fansite."

Star Citizen intellectual property, content, and trademarks are owned by Cloud Imperium Rights LLC, Cloud Imperium Rights Ltd., and their subsidiaries.
