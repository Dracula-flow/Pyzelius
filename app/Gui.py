# Qui creeremo la classe per la GUI usando Tkintr

import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
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
        
        tabs = (
                ("Full", signature), 
                ("Sanity", signature_sanity), 
                ("Simple", signature_minimal)
                )


        for tab_name, signature_class in tabs:
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=f"{tab_name}")

            entry_list = []

            for i, field in enumerate(signature_class.input_fields):
                ttk.Label(tab, text=field).grid(row=i, column=0, padx=10, pady=5)
                entry = ttk.Entry(tab)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry_list.append(entry)

            button = ttk.Button(tab, text="Copia firma (Alt+D)", command=lambda entry_list=entry_list: self.controller.on_copy(entry_list))
            button.grid(row=len(signature_class.input_fields), column=0, columnspan=2, pady=20)



        def bind_hotkey(event, entry_list=entry_list):
            self.controller.on_copy(entry_list)

        tab.bind("<Alt-d>", bind_hotkey)  # Use `tab` as the target for the hotkey binding

            
        tabControl.pack(expand = 1, fill ="both") 


class NotePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.controller =  CT(self)
        self.create_widgets()
    
    def create_widgets(self):
        noteFrame = tk.Frame(self)
        noteFrame.pack(padx=10,pady=10)
        entryField = tk.Text(noteFrame, height=8, width=30)
        entryField.pack(padx=5, pady=5)

        button = ttk.Button(noteFrame, text="Copia nota (Alt+F)", command=lambda: self.controller.copy_text(entryField))
        button.pack(pady=5)

        self.master.bind("<Alt-f>", lambda event: self.controller.copy_text(entryField))

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

        menu_structure = {
            "Nuovo..." : [("Cartella giornaliera", self.controller.new_daily_folder, "Crea una cartella con la data del giorno in cui custodire le evidenze dei test"),
                          ("Cartella Sanity", self.controller.new_sanity_folder, "Crea una cartella per la raccolta e lo smistamento delle evidenze dei Sanity"),
                            ("Report", self.controller.new_report, "Genera un report dei test portati a termine in giornata")],
            "Azioni..." : [("Modifica path", self.controller.new_path_folder, "Modifica il luogo in cui verranno create le cartelle Giornaliere e Sanity"),
                           ("Smista screen Sanity", self.controller.sanity_paste, "Incolla automaticamente gli screenshot Sanity sui file Master della Cartella Sanity")
                           ],
        }

        for label,command in menu_structure.items():
            menu = self.create_submenu(menu_bar, command)
            menu_bar.add_cascade(label=label, menu=menu)

        self.config(menu=menu_bar)

    def create_submenu(self, parent_menu, items):
        """Helper method to create a submenu with commands."""
       
        submenu = tk.Menu(parent_menu, tearoff=0)
       
        for label, command, message in items:
           
            menu_item = submenu.add_command(label=label, command=command)
            submenu.add_separator()  # Add separator between items
            Hovertip(menu_item,message)
        return submenu

    def create_widgets(self):
        sign_panel= SignaturePanel(master=self)
        note_panel= NotePanel(master=self)
        sign_panel.pack(padx=10, pady=10)
        note_panel.pack(padx=10,pady=10)
