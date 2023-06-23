import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar, Canvas


class MovieStreamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Stream Buttons")
        self.geometry("1200x600")
        self.resizable(False, False)  # Disable window resizing

        # Configure dark mode theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', foreground='white', background='black', width=25, padding=5)
        style.configure('TFrame', background='black')

        self.create_movie_buttons()

        # Create a function to scroll the canvas using the scroll wheel
        self.bind_all("<MouseWheel>", self.scroll_canvas)

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
        try:
            print("Fetching source code from:", url)
            response = requests.get(url)
            html_content = response.content

            # Parse the HTML content
            print("Parsing HTML content...")
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all the buttons and extract the URLs and text
            print("Extracting URLs and text from buttons...")
            buttons = soup.find_all("button")
            for button in buttons:
                onclick_attr = button.get("onclick")
                if onclick_attr:
                    url_start_index = onclick_attr.find("'") + 1
                    url_end_index = onclick_attr.rfind("'")
                    url = onclick_attr[url_start_index:url_end_index]
                    text = button.text.strip()

                    button = ttk.Button(
                        self.frame, text=text, command=lambda url=url: self.open_stream(url)
                    )
                    button.grid(
                        row=self.current_row, column=self.current_column, padx=5, pady=5, sticky='w'
                    )
                    button.bind("<Enter>", lambda e, btn=button: btn.configure(background='gray'))
                    button.bind("<Leave>", lambda e, btn=button: btn.configure(background='black'))
                    button.bind("<Button-1>", lambda e, btn=button: btn.configure(background='blue'))
                    button.bind("<Button-1>", lambda e, btn=button: self.scroll_to_button(btn))

                    self.filtered_buttons.append(button)

                    self.current_column += 1
                    if self.current_column >= self.buttons_per_row:
                        self.current_row += 1
                        self.current_column = 0

        except requests.exceptions.RequestException as e:
            print("Error fetching source code:", e)
            messagebox.showerror("Error", "Failed to fetch source code. Please check the URL.")
            self.destroy()

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

    def scroll_canvas(self, event):
        self.frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_to_button(self, button):
        self.frame.update()
        self.frame.yview_moveto(float(button.grid_info()["row"]) / (self.current_row + 1))


if __name__ == "__main__":
    app = MovieStreamApp()
    app.mainloop()
