import tkinter as tk
from tkinter import ttk

from controller import ControllerV3 as CT

class NotePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)
        self.create_widgets()
        
    def create_widgets(self):
        note_frame = tk.Frame(self)
        note_frame.pack(padx=10, pady=10)
        
        self.text_widget = tk.Text(note_frame, height=8, width=25, relief="solid")
        self.text_widget.pack(fill="both", expand=1)

        btn = ttk.Button(note_frame, text="Copia nota (Alt+F)", command=self.copy_note)
        btn.pack(pady=5)

        self.master.bind("<Alt-f>", lambda e: self.copy_note())

    def copy_note(self):
        self.controller.copy_text(self.text_widget.get("1.0", tk.END).strip())
