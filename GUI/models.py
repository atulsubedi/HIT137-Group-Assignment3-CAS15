from tkinter import *
from tkinter.ttk import *


class ModelWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Model Window")
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
