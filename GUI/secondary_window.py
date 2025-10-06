from tkinter import *
from tkinter.ttk import *
from styles import get_text_tags

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
        super().__init__(master, title="Model Information", size="500x400")

        notebook = Notebook(self, style="TNotebook")
        notebook.pack(fill="both", expand=True)

        # === Tab 1: Text Sentiment Model ===
        tab1 = Frame(notebook, style="basic.TFrame")
        notebook.add(tab1, text="Model 1")

        model_desc1 = (
            "This model analyses written text to determine its emotional tone.\n"
            "It classifies the text as positive, negative, or neutral, and provides "
            "a confidence score showing how certain the model is about its prediction.\n"
            "It uses a pre-trained transformer-based pipeline from Hugging Face's "
            "Transformers library for efficient and accurate sentiment classification."
        )

        # Banner title
        tab1_banner = Frame(tab1, style="baner.TFrame")
        tab1_banner.pack(fill='x')
        Label(tab1_banner, text='Text Sentiment Analysis',
              style='banner.TLabel').pack(pady=5)

        # Frame to hold text + scrollbar
        tab1_container = Frame(tab1)
        tab1_container.pack(fill="both", expand=True)
        # Make the text widget expand properly
        tab1_container.grid_rowconfigure(0, weight=1)
        tab1_container.grid_columnconfigure(0, weight=1)

        model_box1 = Text(tab1_container, wrap="word")
        model_box1.grid(row=0, column=0)

        scrollbar1 = Scrollbar(tab1_container, command=model_box1.yview)
        model_box1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.grid(row=0, column=1, sticky="ns")

        # === Tab 2: Image Classification Model ===
        tab2 = Frame(notebook, style="basic.TFrame")
        notebook.add(tab2, text="Model 2")

        text_desc2 = (
            "This model recognises the main object or concept in an image.\n"
            "It uses a Vision Transformer (ViT) architecture to analyse visual content "
            "and predict the most likely label (e.g., cat, car, or flower).\n"
            "The model outputs a predicted class along with a confidence score, "
            "helping users understand the certainty of its identification."
        )

        # Banner title
        tab1_banner = Frame(tab2, style="baner.TFrame")
        tab1_banner.pack(fill='x')
        Label(tab1_banner, text='Image Classification',
              style='banner.TLabel').pack(pady=5)
        # Frame to hold text + scrollbar
        tab2_container = Frame(tab2)
        tab2_container.pack(fill="both", expand=True)
        # Make the text widget expand properly
        tab2_container.grid_rowconfigure(0, weight=1)
        tab2_container.grid_columnconfigure(0, weight=1)

        model_box2 = Text(tab2_container, wrap="word")
        model_box2.grid(row=0, column=0)

        scrollbar2 = Scrollbar(tab2_container, command=model_box2.yview)
        model_box2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=0, column=1, sticky="ns")

        # === Tab 3: Placeholder ===
        tab3 = Frame(notebook, style="basic.TFrame")
        notebook.add(tab3, text="Model 3 (Coming Soon)")

        # Banner title
        tab1_banner = Frame(tab2, style="baner.TFrame")
        tab1_banner.pack(fill='x')
        Label(tab1_banner, text='To Be Determined',
              style='banner.TLabel').pack(pady=5)
        # Frame to hold text + scrollbar
        tab3_container = Frame(tab2)
        tab3_container.pack(fill="both", expand=True)
        # Make the text widget expand properly
        tab3_container.grid_rowconfigure(0, weight=1)
        tab3_container.grid_columnconfigure(0, weight=1)

        model_box3 = Text(tab3_container, wrap="word")
        model_box3.grid(row=0, column=0)

        scrollbar3 = Scrollbar(tab3, command=model_box3.yview)
        model_box3.config(yscrollcommand=scrollbar3.set)
        scrollbar3.grid(row=0, column=1, sticky="ns")

        # Configure text tags for styling
        tags = get_text_tags()
        for tag, opts in tags.items():
            model_box1.tag_configure(tag, **opts)
            model_box2.tag_configure(tag, **opts)
            model_box3.tag_configure(tag, **opts)

        model_box1.insert("1.0", model_desc1, 'body')
        model_box2.insert("1.0", text_desc2, 'body')
        model_box3.insert(
            "1.0", "A future model will be defined here.", 'body')

        model_box1.config(state="disabled")
        model_box2.config(state="disabled")
        model_box3.config(state="disabled")

# ----------------------------------------- INFO WINDOW


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
        info_box = Text(text_frame, wrap='word', font=(
            "Arial", 11))
        info_box.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = Scrollbar(
            text_frame, orient="vertical", command=info_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Link scrollbar and text widget
        info_box.config(yscrollcommand=scrollbar.set)

        # Configure text tags for styling
        tags = get_text_tags()
        for tag, opts in tags.items():
            info_box.tag_configure(tag, **opts)

        # Insert styled content
        info_box.insert("end", "Multiple Inheritance\n", "heading")
        info_box.insert(
            "end", "Used in secondary windows when each secondary window class is called.\nExample: InfoWindow(SecondaryWindow, Transient)\n\n", "body")

        info_box.insert("end", "Encapsulation\n", "heading")
        info_box.insert(
            "end", "Encapsulation is applied to keep all the widgets and layout logic inside each window class. This is done to:\n", "body")
        info_box.insert(
            "end", "• keep code organised in modular and reusable capsules\n", "bullet")
        info_box.insert(
            "end", "• prevent the need to duplicate code throughout the program as you can repeatedly call the same function\n", "bullet")
        info_box.insert(
            "end", "• ease the process of debugging and maintenance as each class manages its own state\n\n", "bullet")

        info_box.insert(
            "end", "Polymorphism and Method Overriding\n", "heading")
        info_box.insert("end", "Polymorphism:\n", "subheading")
        info_box.insert(
            "end", "The same class (SecondaryWindow) produces two different types of windows depending on subclass:\n", "body")
        info_box.insert(
            "end", "• ModelWindow - a tabbed notebook window\n", "bullet")
        info_box.insert(
            "end", "• InfoWindow - a plain information window with a banner\n\n", "bullet")

        info_box.insert("end", "Method Overriding:\n", "subheading")
        info_box.insert(
            "end", "Both subclasses override the __init__ method. They keep the base behaviour via super().__init__, but then add their own widgets.\n\n", "body")

        info_box.insert("end", "Multiple Decorators\n", "heading")
        info_box.insert("end", "Applied in secondary_window.py:\n", "body")
        info_box.insert(
            "end", "• one decorator to validate that the newly opened subwindow has a parent\n", "bullet")
        info_box.insert(
            "end", "• a second decorator that automatically sets the new window in focus\n", "bullet")
        info_box.config(state="disabled")
