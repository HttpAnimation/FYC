import datetime
import html
import time
print("This script is very janky")
print("Thanks to HttpAnimations for making this script")
print("This script is running as 1.0")
time.sleep(0.3)

# Ask user for input
torrent_name = input("Enter the name of the Torrent: ")
torrent_link = input("Enter the link to the torrent file: ")
dir_link = input("Enter the host link to download the torrent: ")
magnet_link = input("Enter the magnet link: ")

# Read the template HTML file
with open("template.html", "r") as file:
    html_template = file.read()

# Replace placeholders with user input
html = html_template.replace("V2TorrentTemplate", torrent_name)
html = html.replace("<!--Link to torrent = ||-->", f"<!--Link to torrent = {torrent_link} -->")
html = html.replace("window.location.href='404Torrent.html'", f"window.location.href='{dir_link}'")
html = html.replace("window.location.href='404Magnet.html'", f"window.location.href='{magnet_link}'")

# Generate filename with timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d-%H%M%S")
filename = f"{torrent_name}_{timestamp}.html"

# Create folder with torrent name if it does not exist
import os
if not os.path.exists(torrent_name):
    os.makedirs(torrent_name)

# Write the new HTML file to folder
with open(f"{torrent_name}/{filename}", "w") as file:
    file.write(html)

print(f"{filename} file has been created successfully!")
print("READ:")
print("1. Rename the .html to a real name")
print("2. Place this file into FYC/FYCRewrite\ Code/ this will give you the js code and style code")
print("Make a button for the button read the discord #guides for it")
print("Discord: https://discord.gg/StHMMFVuGz")
