# Qui creeremo la classe per la GUI usando Tkintr

import tkinter as tk
from app.Controller import Controller as CT

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pyzelius v1.0")
        self.geometry("350x150")

        self.controller = CT(self)
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Label
        self.label = tk.Label(self, text="Defect Title", font=("Arial", 13))
        self.label.pack(pady=20)

        # Casella di testo
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Bottone per prendere l'entry e nominare una cartella per il defect
        self.button = tk.Button(self, text="Crea cartella defect", font=("Arial", 12), command= lambda: self.controller.new_defect_folder(self.entry.get()))
        self.button.pack(pady=10)


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


