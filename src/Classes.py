import csv,os,json
import pandas as pd
import openpyxl as op
from src.Functions import time_responser
from tkinter import filedialog,messagebox,Label,Entry
import tkinter as tk
from pathlib import Path


# Una classe per creare i CSV file da buttare nei dataframe, partendo dai file di una cartella
# Divisione per Defects e Passed
class CSV_File:
    def __init__(self, prefix, path):
        self.prefix = prefix
        self.filename = f"{path}/Report/{self.prefix}_{time_responser('date')}.csv"
    
    # Gli headers hanno bisogno di un argument, di solito, per convenzione credo.
    # Quando non ne hanno bisogno, li si dichiara metodi di classe con questo override, e si scrive cls nei parametri.
    @classmethod
    def passed_headers(cls):
        headers = ["Slot", "OS", "Clone","Test","Retest"]
        return headers

    @classmethod
    def defect_headers(cls):
        headers = ["Slot", "OS", "Clone","Test","Defect ID"]
        return headers
    
    def create_row(self,path):
        # for file in os.listdir(path):
        #     if file.endswith(".mp4"):
        # POtrebbe funzionare?
        final_path = os.path.join(path,self.prefix)
        data = [f for f in os.listdir(final_path) if (os.path.join(final_path, f)) and f.endswith('.mp4')]
        rows = []

        for file in data:
                # Toglie il format al nome del file
                formatted_entry, _ =os.path.splitext(file)
                # Divide ogni nome di file in un singolo array
                entry = formatted_entry.split("-")
                # Mette i diversi array nell'array principale
                rows.append(entry)

        return rows

    def create_file(self, headers, rows):
        # Creazione del file CSV con intestazione e righe di dati
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

# Genera i dataframe dai CVS e li mette in un excel, formattato secondo le esigenze
class Report:
    def __init__(self,path):
        self.date_str = time_responser('date')
        self.path = path
        self.filename = rf"{self.path}/Report_{self.date_str}.xlsx"

    def data_feed(self):
        # Crea un file excel e carica il dataframe sul primo excel sheet
        # It seems like pd.read_csv doesn't like utf-8. latin-1 encoding should solve the problem.
        df_passed = pd.read_csv(rf"{self.path}/Passed_{self.date_str}.csv", encoding='latin-1')
        df_passed.to_excel(self.filename, index=True, sheet_name="Passed")

        # Carica il secondo dataframe su un secondo sheet
        df_defect = pd.read_csv(rf"{self.path}/Defects_{self.date_str}.csv", encoding='latin-1')
        with pd.ExcelWriter(self.filename, engine="openpyxl", mode="a") as writer:
            df_defect.to_excel(writer, index=True,sheet_name="Defects")
        
        # Carica il file excel su openpyxl
        wb = op.load_workbook(self.filename)

        ws1= wb["Passed"]
        ws2= wb["Defects"]

        # Adatta la larghezza delle colonne per il primo foglio
        self.adjust_column_width(ws1)
        
        # Adatta la larghezza delle colonne per il secondo foglio
        self.adjust_column_width(ws2)
        
        # Salva il file Excel con le modifiche
        wb.save(self.filename)

    # Adapts the width of the columns based on the content.
    def adjust_column_width(self, worksheet):
        for col in worksheet.columns:
            try:
                max_length = 0
                column = col[0].column_letter 
                for cell in col:
                        if len(cell.value) > max_length:
                            max_length = max(max_length,len(cell.value))
                adjusted_width = (max_length + 2) 
                worksheet.column_dimensions[column].width = adjusted_width
                # It's gonna raise a TypeError exception anytime there's an empty field in the CSV
                # That's gonna happen sometimes, so it's pass.
            except TypeError:
                pass


    def delete_csv(self,csv_1,csv_2):
        try:
            os.remove(csv_1)
            os.remove(csv_2)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror(title="ERROR!", message=f"An error has occured: {e}")
            
# The WorkTree creates a daily folder with three subfolders named Passed, Defects, and Report.
# Passed and Defects are self-explanatory, Report contains the titular report to be created at the end of the workday.
class WorkTree:
    def __init__(self,path):
        self.path = path
        self.dirname = time_responser('date')
        self.subdirs = ("Passed","Defects", "Report")

    def create_worktree(self):
        root_path = os.path.join(self.path,self.dirname)
        try:
            os.mkdir(root_path)
            messagebox.showinfo(title="Success!", message=f"Folder {self.dirname} created!")
        except FileExistsError:
            messagebox.showerror(title="Error!",message=f"The folder {self.dirname} already exists!")

        for subdir in self.subdirs:
            subdir_path = os.path.join(root_path,subdir)
            os.mkdir(subdir_path)

    # This method creates the singular defect subdir to house both video and debug logs.
    @staticmethod
    def create_subdir(path,dir_name):
        new_dir = os.path.join(path, dir_name)
        try:
            os.mkdir(new_dir)
            messagebox.showinfo(title="Success!", message=f"Defect folder {dir_name} opened!")
        except FileExistsError:
            messagebox.showerror(title="Error!", message=f"Defect folder {dir_name} already opened!")

# A class to get the correct path for the rest of the program
class Pathfinder:
    def __init__(self):
        self.config_last_path = Path(__file__).resolve().parent.parent / 'config/config.json'
        self.last_path = self.load_last_path()

    def load_last_path(self):
        # Load the last used directory path from a configuration file.
        if os.path.exists(self.config_last_path):
            try:
                with open(self.config_last_path, 'r') as config_file:
                    config = json.load(config_file)
                    return config.get("last_path", "")
            except PermissionError:
                print ("Permission error while trying to read the file")
            except json.JSONDecodeError:
                print("Error decoding the configuration file.")
                return ""
        return ""  # Return an empty string if no path was saved

    def save_last_path(self):
        # Save the current directory path to the configuration file.
        config = {"last_path": self.last_path}
        try:
            with open(self.config_last_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
        except PermissionError:
            messagebox.showerror(title="Error!", message="Permission error in attempt to write to the configuration file.")

    def modify_last_path(self):
        # Chiedi all'utente di selezionare una nuova directory
        
        new_path = filedialog.askdirectory()

        if new_path:  # Se l'utente ha selezionato un percorso
            # Carica il file di configurazione esistente
            self.last_path = new_path
            self.save_last_path()

    def get_path(self):
        return self.last_path
    
class Signature():
    def __init__(self):
        self.input_fields = ("Sigla", 
                "ID",
                "APP",
                "BUILD", 
                "DEVICE",
                "OS",
                "Puntamento")
        self.combine=[]

    def entry_combine(self, entry_list):
        self.combine.clear()
        for entry,key in zip(entry_list,self.input_fields):
            try:
                # input_value= entry.get()
                self.combine.append(f"{key} {entry}")
            except TypeError:
                messagebox.showerror (f"Error: Invalid Input - {key}")

        self.combine.append(f"{'DATA E ORA'} {time_responser('datetime')}")
        self.result = "\n".join(self.combine)
        return self.result
    




