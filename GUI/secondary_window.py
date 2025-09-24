from tkinter import *
from tkinter.ttk import *


class SecondaryWindow(Toplevel):
    def __init__(self, master, title, size):
        super().__init__(master)
        self.title(title)
        self.geometry(size)

        # --- Make modal by default
        self.grab_set()
        self.focus_set()
        self.transient(master)   # keeps it on top of parent


# ----------------------------------------- MODEL WINDOW


class ModelWindow(SecondaryWindow):
    def __init__(self, master):
        super().__init__(master, title="Models", size="500x400")
        self.geometry("400x300")

        notebook = Notebook(self, style="TNotebook")
        notebook.pack(fill="both", expand=True)

        # Create 3 pages (frames)
        page1 = Frame(notebook, style="basic.TFrame")
        page2 = Frame(notebook, style="basic.TFrame")
        page3 = Frame(notebook, style="basic.TFrame")

        # Add them as tabs
        notebook.add(page1, text="Model 1")
        notebook.add(page2, text="Model 2")
        notebook.add(page3, text="Model 3")

        # Example content
        Label(page1, text="This is Page 1", font=("Arial", 14)).pack(pady=20)
        Label(page2, text="This is Page 2", font=("Arial", 14)).pack(pady=20)
        Label(page3, text="This is Page 3", font=("Arial", 14)).pack(pady=20)


# ----------------------------------------- INFO WINDOW


class InfoWindow(SecondaryWindow):
    def __init__(self, master):
        super().__init__(master, title="Information", size="400x300")

        self.geometry()

        container = Frame(self, height=400, width=300, style='basic.TFrame')
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        banner = Frame(container, style='banner.TFrame')
        banner.grid(row=0, column=0, columnspan=2, sticky='new')

        title = Label(banner, text='How was OOP applied?',
                      style='banner.TLabel')
        title.pack(pady=5)
