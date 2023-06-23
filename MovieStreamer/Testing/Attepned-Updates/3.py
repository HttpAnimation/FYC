import requests
import tkinter as tk
from tkinter import ttk, Scrollbar, Canvas
from bs4 import BeautifulSoup
import webbrowser

URL = "http://localhost:2345/FYCREWirte%20Code/Movies.html"


class MovieStreamApp:
    def __init__(self, url):
        self.url = url
        self.urls = []
        self.texts = []
        self.filtered_buttons = []

        self.window = tk.Tk()
        self.window.title("Movie Stream Buttons")
        self.window.geometry("1200x600")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', foreground='white', background='black')
        style.configure('TFrame', background='black')

        self.create_search_bar()
        self.create_button_frame()

        self.populate_buttons()

        self.create_scroll_wheel_binding()

    def create_search_bar(self):
        search_frame = ttk.Frame(self.window, padding=10)
        search_frame.pack(side="top", fill="x")

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left")

        clear_button = ttk.Button(search_frame, text="Clear", command=self.clear_search)
        clear_button.pack(side="left", padx=5)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_buttons)
        search_button.pack(side="left", padx=5)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.filter_buttons("")

    def create_button_frame(self):
        canvas = Canvas(self.window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.window, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.button_frame = ttk.Frame(canvas, padding=10)
        canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

    def populate_buttons(self):
        response = requests.get(self.url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        buttons = soup.find_all("button")

        for button in buttons:
            onclick_attr = button.get("onclick")
            if onclick_attr:
                url_start_index = onclick_attr.find("'") + 1
                url_end_index = onclick_attr.rfind("'")
                url = onclick_attr[url_start_index:url_end_index]
                self.urls.append(url)
                self.texts.append(button.text.strip())

    def filter_buttons(self, search_text):
        for button in self.filtered_buttons:
            button.destroy()

        self.filtered_buttons = []
        current_row = 0
        current_column = 0

        for url, text in zip(self.urls, self.texts):
            if search_text.lower() in text.lower():
                button = ttk.Button(
                    self.button_frame,
                    text=text,
                    command=lambda url=url: self.open_stream(url)
                )
                button.grid(row=current_row, column=current_column, padx=5, pady=5, sticky='w')
                self.filtered_buttons.append(button)

                current_column += 1
                if current_column >= 5:  # buttons_per_row
                    current_row += 1
                    current_column = 0

    def open_stream(self, url):
        full_url = f"http://localhost:2345/FYCREWirte%20Code/{url}"
        response = requests.get(full_url)
        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")
        stream_button = soup.find("button", text="Play now (Stream)")
        if stream_button:
            stream_url = stream_button.get("onclick").split("'")[1]
            webbrowser.open(stream_url)

    def search_buttons(self):
        search_text = self.search_entry.get()
        self.filter_buttons(search_text)

    def create_scroll_wheel_binding(self):
        def scroll_canvas(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.window.bind_all("<MouseWheel>", scroll_canvas)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = MovieStreamApp(URL)
    app.run()
