import csv,os
import pandas as pd
import openpyxl as op
from src.Functions import time_responser, get_path

# Una classe per creare i CSV file da buttare nei dataframe, partendo dai file di una cartella
# Divisione per Defects e Passed
class CSV_File:
    def __init__(self, prefix):
        self.prefix = prefix
        self.filename = f"{self.prefix}_{time_responser('date')}.csv"
    
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
    
    def create_row(path):
        data = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
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
    def __init__(self):
        self.filename = f"Report_{time_responser('date')}.xlsx"

    def data_feed(self):
        # Crea un file excel e carica il dataframe sul primo excel sheet
        df_passed = pd.read_csv(rf"{get_path()}\Report\Passed_{time_responser('date')}.csv")
        df_passed.to_excel(self.filename, index=True, sheet_name="Passed")

        # Carica il secondo dataframe su un secondo sheet
        df_defect = pd.read_csv(rf"{get_path()}\Report\Defects_{time_responser('date')}.csv")
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

    def adjust_column_width(self, worksheet):
        # Adatta la larghezza delle colonne in base al contenuto
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter  # Ottiene la lettera della colonna
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)  # Aggiunge un po' di margine
            worksheet.column_dimensions[column].width = adjusted_width

# Crea la directory secondo mie specifiche: una cartella giornaliera e una sottocartella a testa per Passed, Defects, e Report.
# Piccolo problema: la classe funziona e create_subdir riesce a rintracciare il worktree, ma solo finché la dashboard rimane aperta.
#       Nelle tue intenzioni, la dashboard dovrebbe ricordare il path anche quando si chiude. Step per 2.0?
class WorkTree:
    def __init__(self):
        self.path = get_path()
        self.dirname = time_responser('date')
        self.subdirs = ("Passed","Defects", "Report")

    def create_worktree(self):
        root_path = os.path.join(self.path,self.dirname)
        os.mkdir(root_path)

        for subdir in self.subdirs:
            subdir_path = os.path.join(root_path,subdir)
            os.mkdir(subdir_path)

    @staticmethod
    def create_subdir(path,dir_name):
        new_dir = os.path.join(path, dir_name)
        
        # Controlla se la directory esiste già
        if not os.path.exists(new_dir):
            try:
                os.mkdir(new_dir)
                print(f"Directory '{new_dir}' creata con successo.")
            except FileExistsError:
                print(f"La directory '{new_dir}' esiste già.")