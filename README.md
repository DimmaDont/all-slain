# all-slain
Star Citizen Game Log Reader

This program monitors the Star Citizen game log in real-time, reporting player kills, vehicle kills, respawn events, and more.

![example screenshot of the program running in windows console](https://github.com/user-attachments/assets/0fa1d08e-776e-449c-b78b-59bf07c5a20c)

## Usage
1. Start the game, and wait until the EasyAntiCheat splash screen closes and the main game window has appeared.
2. If Star Citizen is installed in the default directory, simply run the program.
2. If Star Citizen is installed elsewhere, move the program into the game folder before running.

Optionally, run the program with the game log file as the first parameter in a terminal.  
For example: `E:\allslain.exe E:\StarCitizen\PTU\Game.log`

> [!TIP]
> The game moves previous log files into the `logbackups` folder.

## Game Version Compatibility
Developed for `4.0_PREVIEW`.  
Mostly compatible with `LIVE` (3.24.3).

## Known Issues
* Antimalware False Positive  
See [pyinstaller's antivirus issue template](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md).  
Workaround: Install Python and run `allslain.py`.

## Disclaimer

"This is an unofficial Fansite."

Star Citizen intellectual property, content, and trademarks are owned by Cloud Imperium Rights LLC, Cloud Imperium Rights Ltd., and their subsidiaries.
