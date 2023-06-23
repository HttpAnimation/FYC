import datetime
from html import escape
import os
import tkinter as tk

# Define GUI window
window = tk.Tk()
window.title("Torrent Generator")
window.geometry("400x400")
window.configure(bg="gray")

# Define GUI elements
label_name = tk.Label(window, text="Torrent Name")
label_name.pack()
entry_name = tk.Entry(window)
entry_name.pack()

label_desc = tk.Label(window, text="Torrent Description")
label_desc.pack()
entry_desc = tk.Entry(window)
entry_desc.pack()

label_link = tk.Label(window, text="Torrent Link")
label_link.pack()
entry_link = tk.Entry(window)
entry_link.pack()

label_dir = tk.Label(window, text="Torrent File Link")
label_dir.pack()
entry_dir = tk.Entry(window)
entry_dir.pack()

label_magnet = tk.Label(window, text="Magnet Link")
label_magnet.pack()
entry_magnet = tk.Entry(window)
entry_magnet.pack()

label_stream = tk.Label(window, text="Stream URL")
label_stream.pack()
entry_stream = tk.Entry(window)
entry_stream.pack()

button_generate = tk.Button(window, text="Generate Torrent", command=lambda: generate_torrent())
button_generate.pack()

label_status = tk.Label(window, text="")
label_status.pack()

def generate_torrent():
    # Get user input
    torrent_name = entry_name.get()
    torrent_desc = entry_desc.get()
    torrent_link = entry_link.get()
    dir_link = entry_dir.get()
    magnet_link = entry_magnet.get()
    stream_url = entry_stream.get()

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

    # Update status label
    label_status.config(text=f"{filename} file has been created successfully!")
    
    # Print the code block at the end
    print(f"Adds {filename},")
    print(f"<!-- {filename} -->")
    print(f'<button class="button" onclick="window.location.href=\'{filename}\'">{filename}</button>')

# Run the GUI
window.mainloop()

