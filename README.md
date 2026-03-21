# hypervdiscordbot
A Discord bot that allows you to remotely turn on your HyperV VM via Discord. This is useful for users who use Easy-GPU-PV and share their resources with other people.

## ※**This bot runs with administration privileges to access the HyperV commands, use with caution!!**
### Prerequisites:
- Installed and running a HyperV VM (You can use [Easy-GPU-PV](https://github.com/jamesstringer90/Easy-GPU-PV/tree/main) for example)
- Python 3.10.x
### Installation:
1. Download the repository and edit the `settings.json` file with the name of your HyperV VM and your Discord bot token.
run.
2. Run `pip install -r requirements.txt` to install the dependencies needed.
3. To run the Discord bot, run the Python script with Administration privileges and let it run in the background.
### Recommended Usage
* Create a venv and make a batch file so you don't have to type on the command line
* Use Task Scheduler to run automatically in the background and have it run when the PC turns on


This was tested on Windows 10 Pro 22H2 running Python 3.10.11

