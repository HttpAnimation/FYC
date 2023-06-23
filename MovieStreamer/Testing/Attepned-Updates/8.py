import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar, Canvas


class MovieStreamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Stream Buttons")
        self.geometry("1200x600")

        # Configure dark mode theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', foreground='white', background='black')
        style.configure('TFrame', background='black')

        self.create_search_bar()
        self.create_movie_buttons()

        # Create a function to scroll the canvas using the scroll wheel
        self.bind_all("<MouseWheel>", self.scroll_canvas)

    def create_search_bar(self):
        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(side="top", anchor="center")

        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side="left")

        def clear_search():
            search_entry.delete(0, tk.END)
            self.filter_buttons("")

        clear_button = ttk.Button(search_frame, text="Clear", command=clear_search)
        clear_button.pack(side="left", padx=5)

        search_button = ttk.Button(search_frame, text="Search", command=self.search_buttons)
        search_button.pack(side="left", padx=5)

        self.search_entry = search_entry

    def create_movie_buttons(self):
        canvas = Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.frame = ttk.Frame(canvas, padding=10)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.buttons_per_row = 5
        self.current_row = 0
        self.current_column = 0
        self.filtered_buttons = []

        # Retrieve the source code from the URL
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

        self.urls = urls
        self.texts = texts

        self.filter_buttons("")

    def filter_buttons(self, search_text):
        print("Filtering buttons with search text:", search_text)
        for button in self.filtered_buttons:
            button.destroy()

        self.filtered_buttons = []
        self.current_row = 0
        self.current_column = 0

        for url, text in zip(self.urls, self.texts):
            if search_text.lower() in text.lower():
                button = ttk.Button(
                    self.frame, text=text, command=lambda url=url: self.open_stream(url)
                )
                button.grid(
                    row=self.current_row, column=self.current_column, padx=5, pady=5, sticky='w'
                )
                self.filtered_buttons.append(button)

                self.current_column += 1
                if self.current_column >= self.buttons_per_row:
                    self.current_row += 1
                    self.current_column = 0

    def open_stream(self, url):
        print("Opening stream for URL:", url)
        import webbrowser

        full_url = "http://localhost:2345/FYCREWirte%20Code/" + url
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

    def scroll_canvas(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == "__main__":
    app = MovieStreamApp()
    app.mainloop()
