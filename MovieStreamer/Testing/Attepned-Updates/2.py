import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import webbrowser

# Retrieve the source code from the URL
# Live updates from a local server
url = "http://localhost:2345/FYCREWirte%20Code/Movies.html"
print("Fetching source code from:", url)
response = requests.get(url)
html_content = response.content

# Parse the HTML content
print("Parsing HTML content...")
soup = BeautifulSoup(html_content, "html.parser")

# Find all the buttons and extract the URLs and text
print("Extracting URLs and text from buttons...")
buttons = soup.find_all("button")
urls = []
texts = []
for button in buttons:
    onclick_attr = button.get("onclick")
    if onclick_attr:
        url_start_index = onclick_attr.find("'") + 1
        url_end_index = onclick_attr.rfind("'")
        url = onclick_attr[url_start_index:url_end_index]
        urls.append(url)
        texts.append(button.text.strip())

# Create a GUI with buttons that open the stream URLs when clicked
print("Creating GUI...")
window = tk.Tk()
window.title("Movie Stream Buttons")
window.geometry("1200x600")

# Configure dark mode theme
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', foreground='white', background='black')
style.configure('TFrame', background='black')

# Create a search bar and clear button
search_frame = ttk.Frame(window, padding=10)
search_frame.pack(side="top", fill="x")

search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side="left")

def clear_search():
    search_entry.delete(0, tk.END)
    filter_buttons("")

clear_button = ttk.Button(search_frame, text="Clear", command=clear_search)
clear_button.pack(side="left", padx=5)

# Create a frame to hold the buttons
frame = ttk.Frame(window, padding=10)
frame.pack(fill="both", expand=True)

# Create buttons with left-to-right layout
buttons_per_row = 5
current_row = 0
current_column = 0
filtered_buttons = []

def filter_buttons(search_text):
    global current_row, current_column, filtered_buttons

    for button in filtered_buttons:
        button.destroy()

    filtered_buttons = []
    current_row = 0
    current_column = 0

    for url, text in zip(urls, texts):
        if search_text.lower() in text.lower():
            button = ttk.Button(frame, text=text, command=lambda url=url: open_stream(url))
            button.grid(row=current_row, column=current_column, padx=5, pady=5, sticky='w')
            filtered_buttons.append(button)

            current_column += 1
            if current_column >= buttons_per_row:
                current_row += 1
                current_column = 0

def open_stream(url):
    full_url = "http://localhost:2345/FYCREWirte%20Code/" + url
    response = requests.get(full_url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    stream_button = soup.find("button", text="Play now (Stream)")
    if stream_button:
        stream_url = stream_button.get("onclick").split("'")[1]
        webbrowser.open(stream_url)

def search_buttons():
    search_text = search_entry.get()
    filter_buttons(search_text)

search_button = ttk.Button(search_frame, text="Search", command=search_buttons)
search_button.pack(side="left", padx=5)

# Populate the initial buttons
filter_buttons("")

# Run the GUI event loop
window.mainloop()
