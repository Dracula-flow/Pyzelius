import tkinter as tk
from tkinter import ttk

import sv_ttk 

from .DeviceManagerWindow import DeviceManagerWindow
from .NotePanel import NotePanel
from .SignaturePanel import SignaturePanel
from .WatcherPanel import WatcherPanel

from controller import ControllerV3 as CT
from src import Localization, SUPPORTED_LANGUAGES

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pyzelius v2.0.0")
        self.geometry("650x680")

        self.controller = CT(self)

        self.configure_styles()
        self.create_menu()
        self.create_layout()

    def configure_styles(self):
        """
        Central place to manage ttk styles for consistent theming.
        """
        style = ttk.Style(self)
        sv_ttk.set_theme("light")  # Try 'clam', 'default', 'alt', or 'vista'

        style.configure("TButton",
                        font=("Arial", 10),
                        padding=6)

        style.configure("TLabel",
                        font=("Arial", 10),
                        padding=4)

        style.configure("TCombobox",
                        font=("Arial", 10),
                        padding=4)

        style.configure("TNotebook",
                        tabposition='n')  # Tabs on top

        style.configure("TNotebook.Tab",
                        font=("Arial", 10, "bold"),
                        padding=[10, 5])

    def create_menu(self):
        """
        Set up the menu bar with nested commands.
        """
        menu_bar = tk.Menu(self)

        menu_structure = {
            _("New..."): [ #type: ignore - it's a builtin, check Localization.py
                (_("Daily folder"), self.controller.new_daily_folder), #type: ignore - it's a builtin, check Localization.py
                (_("Sanity folder"), self.controller.new_sanity_folder), #type: ignore - it's a builtin, check Localization.py
                (_("Report"), self.controller.generate_report), #type: ignore - it's a builtin, check Localization.py
            ],
            _("Actions..."): [ #type: ignore - it's a builtin, check Localization.py
                (_("Change path"), self.controller.update_path), #type: ignore - it's a builtin, check Localization.py
                (_("Sort Sanity screenshots"), self.controller.sanity_paste), #type: ignore - it's a builtin, check Localization.py
                (_("Device Manager"), self.open_device_manager), #type: ignore - it's a builtin, check Localization.py
            ],
        }

        for label, commands in menu_structure.items():
            submenu = self.build_submenu(menu_bar, commands)
            menu_bar.add_cascade(label=label, menu=submenu)

        menu_bar.add_cascade(label=_("Language"), menu=self.build_language_menu(menu_bar)) #type: ignore - it's a builtin, check Localization.py

        self.config(menu=menu_bar)

    def build_submenu(self, parent_menu, items):
        """
        Create a menu with commands and separators between entries.
        """
        submenu = tk.Menu(parent_menu, tearoff=0)
        for i, (label, command) in enumerate(items):
            submenu.add_command(label=label, command=command)
            if i < len(items) - 1:
                submenu.add_separator()
        return submenu

    def build_language_menu(self, parent_menu):
        """
        Builds the "Language" submenu, with a radio-style marker on the
        currently active language. Language names are always shown in
        their own native form (never translated).
        """
        language_menu = tk.Menu(parent_menu, tearoff=0)
        selected_lang = tk.StringVar(value=Localization.get_language())

        for lang_code, native_name in SUPPORTED_LANGUAGES.items():
            language_menu.add_radiobutton(
                label=native_name,
                value=lang_code,
                variable=selected_lang,
                command=lambda code=lang_code: self.controller.change_language(code),
            )
        return language_menu

    def open_device_manager(self):
        """
        Launch the device manager window.
        """
        DeviceManagerWindow(self)

    def create_layout(self):
        """
        Place signature and note panels using consistent padding.
        """
        signature_panel = SignaturePanel(master=self)
        note_panel = NotePanel(master=self)
        watcher_panel = WatcherPanel(master=self)

        signature_panel.grid(row=0,column=1,padx=30,pady=15)
        note_panel.grid(row=1,column=1)
        watcher_panel.grid(row=0,column=2,padx=30)
