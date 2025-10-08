from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.messagebox
from tkinter.messagebox import showinfo
import numpy as np

from secondary_window import InfoWindow, ModelWindow
from styles import setup_styles
from ai_integration import AIIntegration


class Root(Tk):
    def __init__(self):
        super().__init__()

        setup_styles(self)

        self.wm_title('Assignment 3')
        self.geometry("600x450")
        self.minsize(600, 450)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.ai = AIIntegration()

        # === MENUBAR ===
        menubar = Menu(self)
        self.config(menu=menubar)

        menubar.add_command(label="Models", command=self.open_model_window)
        menubar.add_command(label="Info", command=self.open_info_window)
        menubar.add_command(label="HELP!", command=self.help)

        # --------------------- Container
        container = Frame(self, height=450, width=600, style='basic.TFrame')
        container.pack(side='top', fill='both', expand=True)

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
        drop_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        options = ["Text Sentiment", "Image Classification"]
        self.model_selection = StringVar(value=options[0])
        dropdown = OptionMenu(
            banner, self.model_selection, options[0], *options)
        dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        button = Button(banner, text="Load Model",
                        command=self.load, style='banner.TButton')
        button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # ------------------------ In_Frame
        in_frame = LabelFrame(
            container, text="User Input Section", style='basic.TLabelframe')
        in_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10)
        in_frame.grid_columnconfigure(0, weight=1, minsize=100)
        in_frame.grid_columnconfigure(1, weight=1, minsize=220)
        in_frame.grid_columnconfigure(2, weight=1, minsize=220)
        in_frame.grid_rowconfigure(0, weight=1)
        in_frame.grid_rowconfigure(1, weight=1)
        in_frame.grid_rowconfigure(2, weight=1)
        in_frame.grid_rowconfigure(3, weight=1)

        radio_frame = LabelFrame(
            in_frame, text='Input Type', style='mini.TLabelframe')
        radio_frame.grid(row=0, column=0, rowspan=2,
                         sticky='nsew', padx=10, pady=(5, 0))

        self.radio_var = StringVar()
        self.text_radio = Radiobutton(
            radio_frame, text='Text', value="Text", variable=self.radio_var,
            command=self.update_input_mode, style='basic.TRadiobutton')
        self.text_radio.grid(row=0, column=0, sticky="nwe",
                             padx=(2, 0), pady=(2, 0))

        self.image_radio = Radiobutton(
            radio_frame, text='Image', value="Image", variable=self.radio_var,
            command=self.update_input_mode, style='basic.TRadiobutton')
        self.image_radio.grid(row=1, column=0, sticky="swe",
                              padx=(2, 0), pady=(0, 2))

        self.browse_btn = Button(in_frame, text="Browse",
                                 command=self.browse, style='basic.TButton')
        self.browse_btn.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.in_box = Text(in_frame, height=5, wrap='word')
        self.in_box.config(font=("calibri", 11), bg="lightgray", fg="darkgray")
        self.in_box.bind("<<Modified>>", self.check_inbox_content)
        self.in_box.grid(row=0, column=1, rowspan=4,
                         sticky="nsew", padx=(0, 10), pady=5)

        self.preview_label = Label(
            in_frame, text='Image Preview', style='basic.TLabel')
        self.preview_label.config(
            anchor='center', relief='solid', font=('Arial', 12, 'bold'),
            background='lightgray', foreground='darkgrey')
        self.preview_label.grid(
            row=0, column=2, rowspan=3, sticky='nsew',
            padx=(0, 10), pady=5)

        btn_frame = Frame(in_frame, style='basic.TFrame')
        btn_frame.grid(row=3, column=2, sticky='nse', padx=(0, 10))

        run = Button(btn_frame, text='Run model', command=self.run)
        run.grid(row=0, column=1, sticky='e', pady=5)
        clr = Button(btn_frame, text='Clear', command=self.clear)
        clr.grid(row=0, column=2, sticky='e', pady=5)

        # ---------------------- Output section
        out_frame = LabelFrame(
            container, text="Model Output Section", style='basic.TLabelframe')
        out_frame.grid(row=2, column=0, columnspan=2,
                       sticky="nsew", padx=10, pady=(5, 10))
        out_frame.grid_rowconfigure(1, weight=1)
        out_frame.grid_columnconfigure(0, weight=1)

        out_label = Label(out_frame, text='Output Display:',
                          style='basic.TLabel')
        out_label.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(10, 5))

        self.out_box = Text(out_frame, height=8, wrap='word')
        self.out_box.config(font=("calibri", 11))
        self.out_box.grid(row=1, column=0, sticky="nsew",
                          padx=10, pady=(0, 10))

        # Stage groups
        self.radio_widgets = [self.text_radio, self.image_radio]
        self.input_widgets = [self.browse_btn, self.in_box, self.preview_label]
        self.action_widgets = [run, clr]

        for w in self.radio_widgets + self.input_widgets + self.action_widgets:
            w.config(state='disabled')

    # === GUI logic ===
    def load(self):
        model = self.model_selection.get()
        print("Selected:", model)
        if model == 'Text Sentiment':
            self.radio_var.set(value='Text')
            self.text_radio.config(state='enabled')
            self.image_radio.config(state='disabled')
            self.update_input_mode()
        if model == 'Image Classification':
            self.radio_var.set(value='Image')
            self.image_radio.config(state='enabled')
            self.text_radio.config(state='disabled')
            self.update_input_mode()
        return model

    def check_inbox_content(self, event=None):
        self.in_box.edit_modified(False)
        content = self.in_box.get("1.0", "end-1c").strip()
        for w in self.action_widgets:
            w.config(state="normal" if content else "disabled")

    def browse(self):
        selection = self.radio_var.get()

        if selection == "Text":
            file_path = filedialog.askopenfilename(
                title="Select a text file", filetypes=[("Text files", "*.txt")]
            )
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.in_box.config(state="normal", bg="white", fg="black")
                self.in_box.delete("1.0", END)
                self.in_box.insert("1.0", content)
                self.preview_label.config(
                    image="", text="Image Preview",
                    background="lightgray", foreground="darkgrey"
                )
                for w in self.action_widgets:
                    w.config(state="normal")

        elif selection == "Image":
            file_path = filedialog.askopenfilename(
                title="Select an image",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("JPEG files", "*.jpeg"),
                    ("Bitmap files", "*.bmp"),
                    ("All image files", "*.png *.jpg *.jpeg *.bmp"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                self.in_box.config(state="normal")
                self.in_box.delete("1.0", END)
                self.in_box.insert("1.0", file_path)
                self.in_box.config(
                    state="disabled", bg="lightgray", fg="darkgray")
                try:
                    img = Image.open(file_path)
                    print("Image opened")
                    preview = img.copy()
                    preview.thumbnail((220, 220))
                    self.img_preview = ImageTk.PhotoImage(preview)
                    self.preview_label.config(image=self.img_preview)

                    # store input as numpy array for model
                    img = img.resize((224, 224)).convert("RGB")
                    self.model_input = np.array(img) / 255.0
                    print("Image processed and stored")

                    for w in self.action_widgets:
                        w.config(state="normal")

                except Exception as e:
                    print("Failed to open image:", e)

                for w in self.action_widgets:
                    w.config(state="normal")

    def run(self):
        model = self.model_selection.get()
        if model == 'Text Sentiment' or model == 'Image Classification':
            # retrieves current radiobutton selection
            selection = self.radio_var.get()
            if selection == "Text":
                user_text = self.in_box.get("1.0", "end-1c")
                output = self.ai.run_text_model(user_text)
            elif selection == "Image":
                file_path = self.in_box.get("1.0", "end-1c")
                output = self.ai.run_image_model(file_path)
            else:
                output = "Please select input type (Text or Image)."
        else:
            output = "Please Make a model Selection"

        self.out_box.delete("1.0", "end")
        self.out_box.insert("end", output)

    def clear(self):
        self.in_box.config(state="normal")
        self.in_box.delete('1.0', END)
        self.preview_label.config(image="", text="Image Preview")
        self.img_preview = None
        self.model_input = None
        if self.radio_var.get() == "Image":
            self.in_box.config(
                state="disabled", bg="lightgray", fg="darkgray")

    def open_model_window(self):
        ModelWindow(self)

    def open_info_window(self):
        InfoWindow(self)

    def update_input_mode(self):
        self.browse_btn.config(state='normal')
        if self.radio_var.get() == "Image":
            self.in_box.config(state="disabled", bg="lightgray", fg="darkgray")
            self.preview_label.config(background="gray95", foreground="black")
        else:
            self.in_box.config(state="normal", bg="white", fg="black")
            self.preview_label.config(
                background='lightgray', foreground='darkgray')

    def help(self):
        tkinter.messagebox.showinfo(
            'Happy to help.',
            'Select the AI model, choose Text or Image input (depending on the model it may be locked)\nthen click Run model.\n\nOutput will appear below.'
        )


if __name__ == "__main__":
    root = Root()
    root.mainloop()
