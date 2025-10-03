from tkinter import *
from tkinter.ttk import *

# decorator to validate that the subwindow that is being opened has a master


def validate_master(func):
    def wrapper(self, master, *args, **kwargs):
        if master is None:
            raise ValueError("A master (parent) must be provided")
        return func(self, master, *args, **kwargs)
    return wrapper


# decorator to automatically pull focus to the newly opened subwindow
def auto_focus(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.focus_set()
        return result
    return wrapper


# create class to make select windows transient
class Transient:
    def apply_transient(self, master, modal=True):
        if master is None:
            return
        try:
            # keep child on top of master
            self.transient(master)
            # make it modal if requested
            if modal:
                self.grab_set()
            # try to force focus into the new window
            self.focus_force()
        except Exception as e:
            print("TransientMixin.apply_transient():", e)

# ----------------------------------------- BASE SECONDARY WINDOW


class SecondaryWindow(Toplevel, Transient):
    def __init__(self, master, title='', size=None, modal=True):
        super().__init__(master)
        if title:
            self.title(title)
        if size:
            self.geometry(size)
        self.apply_transient(master, modal=modal)

# ----------------------------------------- MODEL WINDOW


class ModelWindow(SecondaryWindow):
    @validate_master
    @auto_focus
    def __init__(self, master):
        super().__init__(master, title="Models", size="500x400")
        self.geometry("400x300")

        notebook = Notebook(self, style="TNotebook")
        notebook.pack(fill="both", expand=True)

        # Create 3 pages (frames)
        page1 = Frame(notebook, style="basic.TFrame")
        page2 = Frame(notebook, style="basic.TFrame")

        # Add them as tabs
        notebook.add(page1, text="Model 1")
        notebook.add(page2, text="Model 2")

        # Example content
        Label(page1, text="Sentiment (Text) \n analysis using hugging face", font=("Arial", 14)).pack(pady=20)
        Label(page2, text="Image classifiaction using \nhugging face model (Vision Transformer)", font=("Arial", 14)).pack(pady=20)


# ----------------------------------------- INFO WINDOW


class InfoWindow(SecondaryWindow):
    @validate_master
    @auto_focus
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


class InfoWindow(SecondaryWindow):
    @validate_master
    @auto_focus
    def __init__(self, master):
        super().__init__(master, title="Information", size="500x300")

        container = Frame(self, style='basic.TFrame')
        container.pack(side='top', fill='both', expand=True)

        # Banner title
        banner = Frame(container, style='banner.TFrame')
        banner.pack(fill='x')
        Label(banner, text='How was OOP applied?',
              style='banner.TLabel').pack(pady=5)

        # Frame to hold text + scrollbar
        text_frame = Frame(container)
        text_frame.pack(fill="both", expand=True)
        # Make the text widget expand properly
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Text widget
        text_box = Text(text_frame, wrap='word', font=(
            "Arial", 11), padx=10, pady=10)
        text_box.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = Scrollbar(
            text_frame, orient="vertical", command=text_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Link scrollbar and text widget
        text_box.config(yscrollcommand=scrollbar.set)

        # Configure text tags for styling
        text_box.tag_configure("heading", font=(
            "Arial", 12, "bold"), spacing3=5)
        text_box.tag_configure("subheading", font=(
            "Arial", 11, "italic"), lmargin1=20, lmargin2=20, spacing1=2)
        text_box.tag_configure("bullet", lmargin1=40, lmargin2=60)
        text_box.tag_configure("body", font=(
            "Arial", 11), lmargin1=20, lmargin2=20, spacing1=2, spacing3=5)

        # Insert styled content
        text_box.insert("end", "Multiple Inheritance\n", "heading")
        text_box.insert(
            "end", "Used in secondary windows when each secondary window class is called.\nExample: InfoWindow(SecondaryWindow, Transient)\n\n", "body")

        text_box.insert("end", "Encapsulation\n", "heading")
        text_box.insert(
            "end", "Encapsulation is applied to keep all the widgets and layout logic inside each window class. This is done to:\n", "body")
        text_box.insert(
            "end", "• keep code organised in modular and reusable capsules\n", "bullet")
        text_box.insert(
            "end", "• prevent the need to duplicate code throughout the program as you can repeatedly call the same function\n", "bullet")
        text_box.insert(
            "end", "• ease the process of debugging and maintenance as each class manages its own state\n\n", "bullet")

        text_box.insert(
            "end", "Polymorphism and Method Overriding\n", "heading")
        text_box.insert("end", "Polymorphism:\n", "subheading")
        text_box.insert(
            "end", "The same class (SecondaryWindow) produces two different types of windows depending on subclass:\n", "body")
        text_box.insert(
            "end", "• ModelWindow – a tabbed notebook window\n", "bullet")
        text_box.insert(
            "end", "• InfoWindow – a plain information window with a banner\n\n", "bullet")

        text_box.insert("end", "Method Overriding:\n", "subheading")
        text_box.insert(
            "end", "Both subclasses override the __init__ method. They keep the base behaviour via super().__init__, but then add their own widgets.\n\n", "body")

        text_box.insert("end", "Multiple Decorators\n", "heading")
        text_box.insert("end", "Applied in secondary_window.py:\n", "body")
        text_box.insert(
            "end", "• one decorator to validate that the newly opened subwindow has a parent\n", "bullet")
        text_box.insert(
            "end", "• a second decorator that automatically sets the new window in focus\n", "bullet")

        # Make text read-only
        text_box.config(state="disabled")
