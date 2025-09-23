from tkinter import *
from tkinter.ttk import *

from models import ModelWindow
from info import InfoWindow
from styles import setup_styles

import tkinter.messagebox
from tkinter.messagebox import showinfo


class Root(Tk):
    def __init__(self):
        Tk.__init__(self)

        setup_styles(self)

        self.wm_title('Assignment 3')
        self.geometry("600x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # === MENUBAR ===
        menubar = Menu(self)
        self.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Option 1")
        file_menu.add_command(label="Option 2")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_command(label="Models", command=self.open_model_window)
        menubar.add_command(label="Info", command=self.open_info_window)
        menubar.add_command(label="Help")

        # --------------------- Container
        # creating a frame and assigning it to the border
        container = Frame(self, height=450, width=600, style='basic.TFrame')
        # specifying the region where the frame is packed in root
        container.pack(side='top', fill='both', expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # --------------------- Banner
        banner = Frame(container, style='banner.TFrame')
        banner.grid(row=0, column=0, columnspan=2, sticky='new')

        banner.grid_columnconfigure(0, weight=1)
        banner.grid_columnconfigure(1, weight=1)

        drop_label = Label(banner, text="Model Selection:",
                           style='banner.TLabel')
        drop_label. grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # Dropdown menu in banner
        options = ["Model 1", "Model 2", "Model 3"]
        self.selected_option = StringVar(value=options[0])
        dropdown = OptionMenu(
            banner, self.selected_option, options[0], *options)
        dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Button in banner
        button = Button(banner, text="Load Model",
                        command=self.on_button_click, style='banner.TButton')
        button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # ------------------------ In_Frame
        in_frame = LabelFrame(
            container, text="User Input Section", style='basic.TLabelframe')
        in_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10)
        in_frame.grid_columnconfigure(
            0, weight=0, minsize=100)

        in_frame.grid_columnconfigure(1, weight=1)
        in_frame.grid_columnconfigure(2, weight=1)

        in_frame.grid_rowconfigure(0, weight=1)
        in_frame.grid_rowconfigure(1, weight=1)
        in_frame.grid_rowconfigure(2, weight=1)
        in_frame.grid_rowconfigure(3, weight=1)

        # Objects in in_frame
        browse = Button(in_frame, text="Browse", style='basic.TButton')
        browse.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=(5, 0))

        self.input_type = StringVar(value="Text")  # default

        text_radio = Radiobutton(
            in_frame, text='Text', value="Text", variable=self.input_type, style='basic.TRadiobutton')
        text_radio.grid(row=1, column=0, sticky="w", padx=(10, 0), pady=(5, 0))

        image_radio = Radiobutton(
            in_frame, text='Image', value="Image", variable=self.input_type, style='basic.TRadiobutton')
        image_radio.grid(row=2, column=0, sticky="w",
                         padx=(10, 0), pady=5)

        file_box = Text(in_frame, height=5, wrap='word')
        file_box.grid(row=0, column=1, rowspan=3, columnspan=2,
                      sticky="nsew", padx=(0, 10), pady=5)

        btn_frame = Frame(in_frame, style='basic.TFrame')
        btn_frame.grid(row=3, column=2, sticky='nse',
                       padx=(0, 10), pady=(0, 5))
        btn_frame.grid_columnconfigure(0, weight=1)
        run1 = Button(btn_frame, text='Run Model 1')
        run1.grid(row=0, column=0, sticky='e')
        run2 = Button(btn_frame, text='Run Model 2')
        run2.grid(row=0, column=1, sticky='e')
        clr = Button(btn_frame, text='Clear')
        clr.grid(row=0, column=3, sticky='e')

        # ---------------------- out_frame
        out_frame = LabelFrame(
            container, text="Model Output Section", style='basic.TLabelframe')
        out_frame.grid(row=2, column=0, columnspan=1,
                       sticky="nsew", padx=10, pady=5)
        out_frame.grid_rowconfigure(1, weight=1)
        out_frame.grid_columnconfigure(0, weight=1)

        out_label = Label(out_frame, text='Output Display:',
                          style='basic.TLabel')
        out_label.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(10, 5))

        out_box = Text(out_frame, height=8, wrap='word')
        out_box.grid(row=1, column=0, sticky="nw", padx=10, pady=(0, 10))

        # ----------------------------- place holder
        place_holder = LabelFrame(
            container, text='placeholder -- (will be substituted)')
        place_holder.grid(row=2, column=1, sticky='nes', padx=10, pady=5)

        place_holder.grid_columnconfigure(0, weight=1)
        place_holder.grid_rowconfigure(1, weight=1)

        out_box = Text(place_holder, height=10, wrap='word')
        out_box.grid(row=1, column=0, sticky="nw", padx=10, pady=10)

    def on_button_click(self):
        print("Selected:", self.selected_option.get())

    def open_model_window(self):
        # Open the secondary window
        ModelWindow(self)

    def open_info_window(self):
        InfoWindow(self)


if __name__ == "__main__":
    root = Root()
    root.mainloop()
