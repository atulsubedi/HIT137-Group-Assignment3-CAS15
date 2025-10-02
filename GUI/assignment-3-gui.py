from tkinter import *
from tkinter.ttk import *

from tkinter import filedialog
from PIL import Image, Image

import numpy as np

from secondary_window import InfoWindow, ModelWindow
from styles import setup_styles

import tkinter.messagebox
from tkinter.messagebox import showinfo


class Root(Tk):
    def __init__(self):
        Tk.__init__(self)

        setup_styles(self)

        self.wm_title('Assignment 3')
        self.geometry("600x450")
        self.minsize(600, 450)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # === MENUBAR ===
        menubar = Menu(self)
        self.config(menu=menubar)
        # define file menu as a submenu on the menubar
        file_menu = Menu(menubar, tearoff=0)
        # define a cascade to contain file commands
        menubar.add_cascade(label="File", menu=file_menu)
        # added commands and separators for file menu
        file_menu.add_command(label="save")
        file_menu.add_command(label="show folder")
        file_menu.add_command(label="change folder")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        # added 2 menu commands on the menubar to create secondary windows
        menubar.add_command(label="Models", command=self.open_model_window)
        menubar.add_command(label="Info", command=self.open_info_window)
        # added 1 menu command on the menubar to call a messagebox to explain functionality
        menubar.add_command(label="HELP!", command=self.help)

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
            0, weight=1, minsize=100)

        in_frame.grid_columnconfigure(1, weight=1, minsize=220)
        in_frame.grid_columnconfigure(2, weight=1, minsize=220)

        in_frame.grid_rowconfigure(0, weight=1)
        in_frame.grid_rowconfigure(1, weight=1)
        in_frame.grid_rowconfigure(2, weight=1)
        in_frame.grid_rowconfigure(3, weight=1)

        # Objects in in_frame
        radio_frame = LabelFrame(in_frame, text='Input Type',
                                 style='mini.TLabelframe')
        radio_frame.grid(row=0, column=0, rowspan=2,
                         sticky='nsew', padx=10, pady=(5, 0))

        radio_frame.grid_rowconfigure(0, weight=1)
        radio_frame.grid_rowconfigure(1, weight=1)

        radio_frame.grid_columnconfigure(0, weight=1)

        self.radio_var = StringVar()  # default

        text_radio = Radiobutton(
            radio_frame, text='Text', value="Text", variable=self.radio_var, command=self.update_input_mode, style='basic.TRadiobutton')
        text_radio.grid(row=0, column=0, sticky="nwe",
                        padx=(2, 0), pady=(2, 0))

        image_radio = Radiobutton(
            radio_frame, text='Image', value="Image", variable=self.radio_var, command=self.update_input_mode, style='basic.TRadiobutton')
        image_radio.grid(row=1, column=0, sticky="swe",
                         padx=(2, 0), pady=(0, 2))

        self.browse_btn = Button(in_frame, text="Browse",
                                 command=self.browse, style='basic.TButton')
        self.browse_btn.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.in_box = Text(in_frame, height=5, wrap='word')
        self.in_box.config(font=("calibri", 11), bg="lightgray", fg="darkgray")
        self.in_box.bind("<<Modified>>", self.check_inbox_content)
        self.in_box.grid(row=0, column=1, rowspan=4, columnspan=1,
                         sticky="nsew", padx=(0, 10), pady=5)

        self.preview_label = Label(
            in_frame, text='Image Preview', style='basic.TLabel')
        self.preview_label.config(
            anchor='center', relief='solid', font=('Arial', 12, 'bold'))
        self.preview_label.config(
            background='lightgray', foreground='darkgrey')
        self.preview_label.grid(
            row=0, column=2, rowspan=3, columnspan=1, sticky='nsew', padx=(0, 10), pady=5)

        btn_frame = Frame(in_frame, style='basic.TFrame')
        btn_frame.grid(row=3, column=2, sticky='nse',
                       padx=(0, 10))

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=100)

        """
        run1 = Button(btn_frame, text='Run model 1')
        run1.grid(row=0, column=0, sticky='e', pady=5)
        """
        run2 = Button(btn_frame, text='Run model', command=self.run)
        run2.grid(row=0, column=1, sticky='e', pady=5)
        clr = Button(btn_frame, text='Clear', command=self.clear)
        clr.grid(row=0, column=2, sticky='e', pady=5)

        # ---------------------- out_frame
        out_frame = LabelFrame(
            container, text="Model Output Section", style='basic.TLabelframe')
        out_frame.grid(row=2, column=0, columnspan=1,
                       sticky="nsew", padx=10, pady=(5, 10))
        out_frame.grid_rowconfigure(1, weight=1)
        out_frame.grid_columnconfigure(0, weight=1)

        out_label = Label(out_frame, text='Output Display:',
                          style='basic.TLabel')
        out_label.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(10, 5))

        out_box = Text(out_frame, height=8, wrap='word')
        out_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # ----------------------------- place holder
        place_holder = LabelFrame(
            container, text='placeholder -- (will be substituted)')
        place_holder.grid(row=2, column=1, sticky='nes', padx=10, pady=(5, 10))

        place_holder.grid_columnconfigure(0, weight=1)
        place_holder.grid_rowconfigure(1, weight=1)

        out_box = Text(place_holder, height=10, wrap='word')
        out_box.grid(row=1, column=0, sticky="nw", padx=10, pady=10)

        # Stage groups
        self.radio_widgets = [text_radio, image_radio]
        self.input_widgets = [self.browse_btn, self.in_box, self.preview_label]
        # buttons at bottom
        self.action_widgets = [run2, clr]
        for w in self.radio_widgets + self.input_widgets + self.action_widgets:
            w.config(state='disabled')

    def on_button_click(self):
        print("Selected:", self.selected_option.get())
        for w in self.radio_widgets:
            w.config(state="normal")

    def check_inbox_content(self, event=None):
        self.in_box.edit_modified(False)
        content = self.in_box.get("1.0", "end-1c").strip()
        if content:
            for w in self.action_widgets:
                w.config(state="normal")
        else:
            for w in self.action_widgets:
                w.config(state="disabled")

    def browse(self):
        selection = self.radio_var.get()
        if selection == "Text":
            file_path = filedialog.askopenfilename(
                initialdir='/', title='Select an image', filetypes=[("Text files", "*.txt")])
        elif selection == "Image":
            file_path = filedialog.askopenfilename(
                initialdir='/', title='Select an image', filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])

        if file_path:
            self.in_box.config(state="normal")
            self.in_box.delete('1.0', END)
            self.in_box.insert(INSERT, file_path)

            if selection == "Image":
                self.in_box.config(
                    state="disabled", bg="lightgray", fg="darkgray")
            else:
                self.preview_label.config(
                    background='lightgray', foreground='darkgray')
            img = Image.open(file_path)
            preview = img.copy()
            preview.thumbnail((220, 220))  # keep aspect ratio

            # Convert to Tkinter image and store reference
            self.img_preview = ImageTk.PhotoImage(preview)
            self.preview_label.config(image=self.img_preview)

            # Store model input as array for later
            img = img.resize((224, 224)).convert("RGB")
            self.model_input = np.array(img) / 255.0

            # set state of action widgets to normal
            for w in self.action_widgets:
                w.config(state="normal")

    def run(self):
        # defines text_input as content in text box
        """
        might be a good idea to check what radiobutton is active (text/image)
        then run separate functions for both or both combined in this function separated by an if statement
        either or is good
        """
        text_input = self.in_box.get("1.0", "end-1c")
        print(text_input)

        """this function will then run the required functions from other files provided by team to return the AI output as output"""

    def clear(self):
        self.in_box.config(state="normal")
        self.in_box.delete('1.0', END)
        # remove image & text
        self.preview_label.config(image="", text="Image Preview")
        # drop reference
        self.img_preview = None
        # also clear file path
        self.in_box.delete("1.0", END)
        self.model_input = None
        if self.radio_var.get() == "Image":
            self.in_box.config(
                state="disabled", bg="lightgray", fg="darkgray")

    def open_model_window(self):
        # Open the secondary window
        ModelWindow(self)

    def open_info_window(self):
        InfoWindow(self)

    def update_input_mode(self):
        self.browse_btn.config(state='enabled')
        if self.radio_var.get() == "Image":
            self.in_box.config(state="disabled", bg="lightgray", fg="darkgray")
            self.preview_label.config(background="gray95",
                                      foreground="black")
        else:
            self.in_box.config(state="normal", bg="white", fg="black")
            self.preview_label.config(
                background='lightgray', foreground='darkgray')

    def help(self):
        tkinter.messagebox.showinfo('Happy to help.',
                                    'Simply select the AI model you wish to use, then in the Input section select the input type you need, enter the information and click run model.\n\nOnce the AI has finished thinking, an output will be displayed in the output section below!')


if __name__ == "__main__":
    root = Root()
    root.mainloop()

# ------------------------------------ spare code

"""prediction = model.predict(np.expand_dims(self.model_input, axis=0))
"""
