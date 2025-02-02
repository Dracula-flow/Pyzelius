# Qui creeremo la classe per la GUI usando Tkintr

import tkinter as tk
from tkinter import Label,Entry
from app.Controller import Controller as CT
from src.Classes import Signature as SI
import pyperclip

class SignaturePanel(tk.Frame):
    def __init__(self, master=None, logic= None):
        super().__init__(master)
        self.master = master
        self.logic = logic or SI() # Usa la logica passata o la default
        self.input_fields = self.logic.input_fields
        self.entry_list = []
        self.create_widgets()

    def create_widgets(self):
        for field in self.input_fields:
            label = Label(self, text=field)
            label.pack()
            entry = Entry(self)
            entry.pack()
            self.entry_list.append(entry)

        self.copy_button = tk.Button(self, text="Copia firma", command=self.on_copy)
        self.copy_button.pack()

        self.label_confirm = tk.Label(self, text="")
        self.label_confirm.pack()

    
    def on_copy(self):
        # Estrai i dati dai campi di input
        entry_values = [entry.get() for entry in self.entry_list]
        
        # Usa la logica per combinare i dati
        result = self.logic.entry_combine(entry_values)

        pyperclip.copy(result)

        self.label_confirm.config(text="Firma copiata!")



class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pyzelius v1.0")
        self.geometry("350x150")

        self.controller = CT(self)
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        
        menu_bar= tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Cartella giornaliera", command= self.controller.new_daily_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Report", command= self.controller.new_report)
        
        menu_bar.add_cascade(label="Nuovo...", menu=file_menu)


        mod_menu= tk.Menu(menu_bar, tearoff=0)
        mod_menu.add_command(label="Destinazione Cart.giorn.", command= self.controller.new_path_folder)

        menu_bar.add_cascade(label="Modifica...", menu=mod_menu)

        self.config(menu=menu_bar)

    def create_widgets(self):
        sign_panel= SignaturePanel(master=self)
        sign_panel.pack(padx=10, pady=10)
