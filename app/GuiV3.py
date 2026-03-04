import tkinter as tk
from tkinter import ttk

from .DeviceManagerWindow import DeviceManagerWindow
from .NotePanel import NotePanel
from .SignaturePanel import SignaturePanel
from .WatcherPanel import WatcherPanel

from controller import ControllerV3 as CT

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pyzelius v1.8.0")
        self.geometry("360x650")

        self.controller = CT(self)

        self.configure_styles()
        self.create_menu()
        self.create_layout()

    def configure_styles(self):
        """
        Central place to manage ttk styles for consistent theming.
        """
        style = ttk.Style(self)
        style.theme_use("vista")  # Try 'clam', 'default', 'alt', or 'vista'

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
            "Nuovo...": [
                ("Cartella giornaliera", self.controller.new_daily_folder),
                ("Cartella Sanity", self.controller.new_sanity_folder),
                ("Report", self.controller.generate_report),
            ],
            "Azioni...": [
                ("Modifica path", self.controller.update_path),
                ("Smista screen Sanity", self.controller.sanity_paste),
                ("Device Manager", self.open_device_manager),
            ],
        }

        for label, commands in menu_structure.items():
            submenu = self.build_submenu(menu_bar, commands)
            menu_bar.add_cascade(label=label, menu=submenu)

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
