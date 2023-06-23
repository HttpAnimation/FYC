import datetime
from html import escape
import time
import os

print("This script is very janky")
print("Thanks to HttpAnimations for making this script")
print("This script is running as 1.0")
time.sleep(0.3)

# Ask user for input
torrent_name = input("Enter the name of the Torrent: ")
torrent_desc = input("Enter the description of the Torrent: ")
torrent_link = input("Enter the host link of the torrent 1337 as exp: ")
dir_link = input("Enter the link to the torrent file: ")
magnet_link = input("Enter the magnet link: ")
stream_url = input("Enter the URL for the stream (or leave blank if none): ")

# Read the template HTML file
with open("template.html", "r") as file:
    html_template = file.read()

# Replace placeholders with user input
html = html_template.replace("V2TorrentTemplate", torrent_name)
html = html.replace("Theres no Description for this torrent", f"{escape(torrent_desc)}")
html = html.replace("<!--Link to torrent = ||-->", f"<!--Link to torrent = {escape(torrent_link)} -->")
html = html.replace("window.location.href='404Torrent.html'", f"window.location.href='{dir_link}'")
html = html.replace("window.location.href='404Magnet.html'", f"window.location.href='{magnet_link}'")
html = html.replace("window.location.href='404Steam.html'", f"window.location.href='{stream_url}'")

# Generate filename with timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d-%H%M%S")
filename = f"{torrent_name}.html"

# Create folder with torrent name if it does not exist
if not os.path.exists(torrent_name):
    os.makedirs(torrent_name)

# Write the new HTML file to folder
with open(f"{torrent_name}/{filename}", "w") as file:
    file.write(html)

print(f"{filename} file has been created successfully!")
print("READ:")
print("1. Rename the .html to a real name")
print("2. Edit the description in the generated HTML file as desired")
print("3. Place this file into FYC/FYCRewrite\ Code/ this will give you the js code and style code")
print("4. Make a button for the button read the discord #guides for it")
print("Discord: https://discord.gg/StHMMFVuGz")

# Print the code block at the end
print(f"Adds {filename},")
print(f"<!-- {filename} -->")
print(f'<button class="button" onclick="window.location.href=\'{filename}\'">{filename}</button>')

