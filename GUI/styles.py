from tkinter.ttk import Style


def setup_styles(root):
    style = Style(root)

    # Use a theme that allows full styling
    style.theme_use("clam")

    # Banner style
    style.configure(
        'banner.TFrame',
        background='steelblue2'
    )
    style.configure(
        'banner.TLabel',
        background='steelblue2',
        foreground='white',
        font=("Arial", 12, "bold")
    )

    # Basic frame style
    style.configure(
        'basic.TFrame',
        background='gray95'
    )
    style.configure(
        'basic.TLabel',
        background='gray95',
        font=('Arial', 10)
    )
    style.configure(
        'basic.TRadiobutton',
        background='gray95',
        font=('Arial', 10)
    )

    # LabelFrame (sections)
    style.configure(
        "basic.TLabelframe",
        background="gray95",
        bordercolor="black",
        borderwidth=3,
        relief="groove"
    )
    style.configure(
        "basic.TLabelframe.Label",
        background="gray95",
        foreground="black",
        font=("Arial", 12, "bold")
    )
    style.configure(
        "mini.TLabelframe",
        background="gray95",
        bordercolor="black",
        borderwidth=3,
        relief="groove"
    )
    style.configure(
        "mini.TLabelframe.Label",
        background="gray95",
        foreground="black",
        font=("Arial", 10, "bold")
    )

    # Notebook
    style.configure("TNotebook",
                    background="steelblue2",
                    borderwidth=2)
    style.configure("TNotebook.Tab",
                    background="steelblue1",
                    foreground="gray97",
                    padding=[10, 5],
                    font=("Arial", 10, 'bold'))
    style.map("TNotebook.Tab",
              background=[("selected", "gray95"),
                          ("active", "gray97")],
              foreground=[("selected", "black"), ("active", "black")])

    return style


def get_text_tags():
    return {
        "heading": {
            "font": ("Arial", 12, "bold"),
            "spacing3": 5,
        },
        "subheading": {
            "font": ("Arial", 11, "italic"),
            "lmargin1": 40,
            "lmargin2": 20,
            "spacing1": 2,
        },
        "bullet": {
            "lmargin1": 40,
            "lmargin2": 60,
        },
        "body": {
            "font": ("Arial", 11),
            "lmargin1": 20,
            "lmargin2": 20,
            "spacing1": 2,
            "spacing3": 5,
        }
    }
