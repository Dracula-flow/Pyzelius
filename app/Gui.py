# Qui creeremo la classe per la GUI usando Tkintr

import tkinter as tk
from tkinter import ttk
from app.Controller import Controller as CT
from src.Classes import Signature, SignatureSanity, SignatureMinimal

class SignaturePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.controller =  CT(self)
        self.create_widgets()

    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        
        signature = Signature()
        signature_sanity = SignatureSanity()
        signature_minimal = SignatureMinimal()
        
        tabs = [
                ("Full", signature), 
                ("Sanity", signature_sanity), 
                ("Simple", signature_minimal)
                ]

        self.entry_list_dict = {}

        for tab_name, signature_class in tabs:
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=f"{tab_name}")

            entry_list = []

            for i, field in enumerate(signature_class.input_fields):
                ttk.Label(tab, text=field).grid(row=i, column=0, padx=10, pady=5)
                entry = ttk.Entry(tab)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry_list.append(entry)

            button = ttk.Button(tab, text="Copia firma", command=lambda entry_list=entry_list: self.controller.on_copy(entry_list))
            button.grid(row=len(signature_class.input_fields), column=0, columnspan=2, pady=20)

            
        tabControl.pack(expand = 1, fill ="both") 

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pyzelius v1.5")
        self.geometry("360x320")

        self.controller = CT(self)
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        
        menu_bar= tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Cartella giornaliera", command= self.controller.new_daily_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Report", command= self.controller.new_report)
        file_menu.add_separator()
        file_menu.add_command(label="Cartella Sanity", command= self.controller.new_sanity_folder)
        
        menu_bar.add_cascade(label="Nuovo...", menu=file_menu)


        mod_menu= tk.Menu(menu_bar, tearoff=0)
        mod_menu.add_command(label="Destinazione Cart.giorn.", command= self.controller.new_path_folder)
        # file_menu.add_separator()
        # mod_menu.add_command(label="Smista screen sanity", command=self.controller.new_sanity_doc)

        menu_bar.add_cascade(label="Modifica...", menu=mod_menu)

        self.config(menu=menu_bar)

    def create_widgets(self):
        sign_panel= SignaturePanel(master=self)
        sign_panel.pack(padx=10, pady=10)
