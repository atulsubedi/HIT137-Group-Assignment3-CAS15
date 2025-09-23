from tkinter import *
from tkinter.ttk import *


class InfoWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Information Window")
        self.geometry("400x300")

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
