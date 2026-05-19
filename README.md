# DiscordAutoSernder

A lightweight GUI application built with Python and Tkinter, designed to automate sending trade messages in Discord channels.

Originally created for games like Deepwoken where you need to constantly post trade offers in multiple hubs, this tool runs in the background and posts your messages automatically. It includes randomized delays to make the activity look more human and prevent rate-limiting or spam flags.

Features

Clean, responsive GUI based on the Catppuccin Mocha dark theme.

Automated sending loop with randomized cooldowns (e.g., 2-3 minutes).

Smart rate-limit handling (automatically pauses if Discord sends a 429 error).

Local storage for your Discord token, message formatting, and channel lists.

Multi-channel support (send to as many channels as you want in one loop).

Built-in message editor that supports Discord markdown and ANSI color codes.

Prerequisites

Python installed on your system.

The requests library.

Installation & Setup

Download or clone this repository to your local machine.

If you are on Windows, make sure to check "Add Python to PATH" during the Python installation.

Open your terminal or command prompt and install the required library by running:
pip install requests

On Windows, you can rename trade_sender.py to trade_sender.pyw. This will make the application run natively without opening a background console window.

Double-click the file to launch the application.

How to Use

Click the TOKEN button and paste your Discord user token. This is saved locally in a trade_token.txt file.

Click the CHANNELS button to add your target channels. Use the format ChannelID=Custom Name so the logs look clean (for example: 921978118523220039=Deepwoken Main Hub).

Click the MESSAGE button to paste your trade offer. It supports all standard Discord formatting, including headers and code blocks.

Click SEND to fire the message once manually.

Click AUTO: OFF to toggle the automatic loop. The button will turn green, and the script will begin rotating through your channels with a randomized sleep timer between each loop.

Disclaimer

Automating a normal Discord user account (self-botting) is against Discord's Terms of Service. This script is provided for educational purposes and personal use only. The randomized timers help avoid automated spam detection, but you use this tool entirely at your own risk. The developer is not responsible for any account bans or restrictions.
