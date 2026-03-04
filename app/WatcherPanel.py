import tkinter as tk
from tkinter import ttk

from controller import ControllerV3 as CT

class WatcherPanel(tk.Frame):
    """
    A tab to house the Watcher/Auto-renamer
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Renamer template:").grid(row=0, column=1)
        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=1, pady=5)
        self.status_label = ttk.Label(self, text="Renamer: OFF")
        self.status_label.grid(row=2,column=1)

        self.start_button = ttk.Button(self, text="Start", command=lambda: self.controller.start_watching(self.entry, self.status_label))
        self.start_button.grid(row=3,column=1,pady=5)

        self.stop_button = ttk.Button(self, text="Stop", command=lambda: self.controller.stop_watching(self.status_label))
        self.stop_button.grid(row=4, column=1,pady=5)

