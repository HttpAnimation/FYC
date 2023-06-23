import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

def extract_info():
    link = link_entry.get()
    if not link:
        messagebox.showerror("Error", "Please enter a 1337x.to link.")
        return

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.find('div', class_='box-info-heading').find('h1').text.strip()
        description = soup.find('div', class_='box-info-description').find('p').text.strip()
        magnet_link = soup.find('a', href=lambda href: href and href.startswith('magnet:')).get('href')
        stream_link = soup.find('a', id='lf5d2f65a9a82ac814de9337f2a06c6030e49bd38').get('href')

        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        description_text.delete(1.0, tk.END)
        description_text.insert(tk.END, description)
        magnet_link_entry.delete(0, tk.END)
        magnet_link_entry.insert(0, magnet_link)
        stream_link_entry.delete(0, tk.END)
        stream_link_entry.insert(0, stream_link)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_text(entry):
    entry_text = entry.get()
    if entry_text:
        root.clipboard_clear()
        root.clipboard_append(entry_text)
        messagebox.showinfo("Copied", "Text has been copied to the clipboard.")

def save_to_file():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please extract the name before saving.")
        return

    try:
        with open(f"{name}.txt", "w") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Description:\n{description_text.get(1.0, tk.END)}")
            file.write(f"Magnet Link: {magnet_link_entry.get()}\n")
            file.write(f"Stream Link: {stream_link_entry.get()}\n")
        messagebox.showinfo("File Saved", f"The information has been saved as {name}.txt.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Torrent Extracter")
root.configure(bg="#121212")
root.geometry("600x400")

# Create the input label and entry
link_label = ttk.Label(root, text="1337x.to Link:", background="#121212", foreground="#ffffff")
link_label.pack(pady=10)
link_entry = ttk.Entry(root, width=50)
link_entry.pack()

# Create the extract button
extract_button = ttk.Button(root, text="Extract", command=extract_info)
extract_button.pack(pady=10)

# Create the name label and entry
name_label = ttk.Label(root, text="Name:", background="#121212", foreground="#ffffff")
name_label.pack()
name_entry = ttk.Entry(root, width=50)
name_entry.pack()

# Create the description label and text box
description_label = ttk.Label(root, text="Description:", background="#121212", foreground="#ffffff")
description_label.pack()
description_text = tk.Text(root, width=50, height=8, wrap="word")
description_text.pack()

# Create the magnet link label and entry
magnet_link_label = ttk.Label(root, text="Magnet Link:", background="#121212", foreground="#ffffff")
magnet_link_label.pack()
magnet_link_entry = ttk.Entry(root, width=50)
magnet_link_entry.pack()

# Create the stream link label and entry
stream_link_label = ttk.Label(root, text="Stream Link:", background="#121212", foreground="#ffffff")
stream_link_label.pack()
stream_link_entry = ttk.Entry(root, width=50)
stream_link_entry.pack()

# Create the copy buttons
copy_name_button = ttk.Button(root, text="Copy Name", command=lambda: copy_text(name_entry))
copy_name_button.pack(pady=10)
copy_magnet_button = ttk.Button(root, text="Copy Magnet Link", command=lambda: copy_text(magnet_link_entry))
copy_magnet_button.pack(pady=5)
copy_stream_button = ttk.Button(root, text="Copy Stream Link", command=lambda: copy_text(stream_link_entry))
copy_stream_button.pack(pady=5)

# Create the save button
save_button = ttk.Button(root, text="Save as .txt", command=save_to_file)
save_button.pack(pady=10)

# Run the main event loop
root.mainloop()
