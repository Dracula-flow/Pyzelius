import csv,os,json,sys
from pathlib import Path

import pandas as pd
import openpyxl as op
from docx import Document
from docx.shared import Inches
from PIL import Image
from tkinter import filedialog,messagebox

from src.Functions import time_responser, format_checker, truncate_path

class CSV_File:
    """
    Creates two CSV files, using as basis the video files present in a folder. This class works together with the 'Report' class.
    """
    def __init__(self, prefix, path):
        self.prefix = prefix
        self.filename = f"{path}/Report/{self.prefix}_{time_responser('date')}.csv"
    
    @classmethod
    def passed_headers(cls):
        headers = ["Slot", "OS", "Clone","Test","Retest"]
        return headers

    @classmethod
    def defect_headers(cls):
        headers = ["Slot", "OS", "Clone","Test","Defect ID"]
        return headers
    
    def create_row(self,path):
        """
        Creates an array of data based on the files in the directory passed to the method.
        """
        final_path = os.path.join(path,self.prefix)
        data = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path, f)) and format_checker(f, '.mp4','.mov')]
        rows = []

        for file in data:
            # Expunges the format from the file name
            formatted_entry, _ =os.path.splitext(file)
            
            entry = formatted_entry.split("-")
            
            rows.append(entry)

        return rows

    def create_file(self, headers, rows):
        """
        Writes the CSV file with the specified parameters.
        """
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

# ---------------------------------------------------------------------------------------------------------------
class Report:
    """
    Creates an .xlsx file, printing two Pandas Dataframes on two different sheets. 
    The data in the dataframes must be supplied via the CSV_File class.
    """
    def __init__(self,path):
        self.date_str = time_responser('date')
        self.path = path
        self.filename = rf"{self.path}/Report_{self.date_str}.xlsx"

    def data_feed(self):
        """
        Creates the .xlsx file and loads the data from the CSV into it.
        """
        # pd.read_csv doesn't like utf-8. latin-1 encoding solves the problem.
        try:
            # Writes the Passed data
            df_passed = pd.read_csv(rf"{self.path}/Passed_{self.date_str}.csv", encoding='latin-1')
            df_passed.to_excel(self.filename, index=True, sheet_name="Passed")

            # Writes the Defects data
            df_defect = pd.read_csv(rf"{self.path}/Defects_{self.date_str}.csv", encoding='latin-1')
            with pd.ExcelWriter(self.filename, engine="openpyxl", mode="a") as writer:
                df_defect.to_excel(writer, index=True,sheet_name="Defects")
            
            # Loads the sheets to an Openpyxl workbook
            wb = op.load_workbook(self.filename)

            # Defines the two sheets inside the file
            ws1= wb["Passed"]
            ws2= wb["Defects"]

            # Formats the columns
            self.adjust_column_width(ws1)
            self.adjust_column_width(ws2)
            
            # Saves the file
            wb.save(self.filename)
            messagebox.showinfo(title="Report creato!", message=f"Il report {self.date_str} è stato creato con successo!")

        except pd.errors.ParserError:
            messagebox.showerror(title="Error!", message="A file does not respect the format!")

    def adjust_column_width(self, worksheet):
        """
        Adapts the width of the columns based on the content.
        """
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
        """
        Deletes the CSV files. To be used after Report generation.
        """
        try:
            os.remove(csv_1)
            os.remove(csv_2)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror(title="ERROR!", message=f"An error has occured: {e}")
            
# ------------------------------------------------------------------------------------------------------------------------

class WorkTree:
    """
    Creates a directory named after the day, with three sub-directories named Passed, Defects and Report.
    Passed and Defects will contain the video test-evidence, Report will host the Report generated via the "Report" class.
    """
    def __init__(self,path):
        self.path = path
        self.dirname = time_responser('date')
        self.subdirs = ("Passed","Defects", "Report")

    def create_worktree(self):
        root_path = os.path.join(self.path,self.dirname)
        try:
            os.mkdir(root_path)
            messagebox.showinfo(title="Cartella creata!", message=f"Cartella {self.dirname} creata!")
        except FileExistsError:
            messagebox.showerror(title="Errore!",message=f"La cartella {self.dirname} esiste già nella destinazione!")

        for subdir in self.subdirs:
            subdir_path = os.path.join(root_path,subdir)
            os.mkdir(subdir_path)

# -------------------------------------------------------------------------------------------------------------------

class Pathfinder:
    """
    Registers the user's preferred destination for the test evidence and allows its modification. 

    The data will be registered into a .JSON file.
    
    While in source code mode, it will default to the "config/config.json" file present in the root.
    
    While in executable mode, if absent, it will create and default to a "pyzelius_config" folder in the Home directory.

    If the path is modified, the app will need to be restarted.

    """
    def __init__(self):
        self.config_last_path = self.get_config_path()
        self.last_path = self.load_last_path()

    def get_config_path(self):
        """
        Returns the path to the configuration file, ensuring it's writable.
        """
        if hasattr(sys, '_MEIPASS'):
            # If running as a bundled executable, save it to the user's home directory or app-specific folder
            config_folder = os.path.join(os.path.expanduser('~'), 'pyzelius_config')
            if not os.path.exists(config_folder):
                os.makedirs(config_folder)
            return os.path.join(config_folder, 'config.json')
        else:
            # If running as a Python script, use the relative path
            return Path(__file__).resolve().parent.parent / 'config/config.json'
        
    def load_last_path(self):
        """
        Load the last used directory path from a configuration file.
        """
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
        """
        Save the current directory path to the configuration file.
        """
        config = {"last_path": self.last_path}
        try:
            with open(self.config_last_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
        except PermissionError:
            messagebox.showerror(title="Error!", message="Permission error in attempt to write to the configuration file.")

    def modify_last_path(self):
        """
        Allows the user to modify the preferred path.
        """
        
        new_path = filedialog.askdirectory()

        if new_path:
            self.last_path = new_path
            self.save_last_path()

    def get_path(self):
        return self.last_path
    
# --------------------------------------------------------------------------------------------------------------------

class Signature():
    """
    Generates a signature necessary to close a test. It has to be mounted on a Tkinter frame.
    """
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
    
class SignatureSanity(Signature):
    """
    Signature subclass with fewer fields.
    """
    def __init__(self):
        super().__init__()
        self.input_fields = ("Sigla", "ID", "CLONE", "BROWSER")  # Subclass with fewer fields

class SignatureMinimal(Signature):
    """
    Signature class with just the initials.
    """
    def __init__(self):
        super().__init__()
        self.input_fields = ("Sigla",)  # The comma is necessary, otherwise the entry_combine will interpret this as a string to split
# -----------------------------------------------------------------------------------------------------------------------------------------

class Master:
    """
    Creates a directory based on a .xlsx file.

    The directory will consist of a main dir called "Sanity" and a variable number of subdirectories 
    each named after the rows in a specific column.

    Each subdirectory will have a "Screenshots" folder and a .docx file named "Master", with some 
    preformatted text (mainly the title, same as the subfolder).
    """
    def __init__(self, path):

        self.path = path
        self.screen_path= None
        self.df = None
        self.doc_path= None

    def new_master_dir(self):
        """
        Creates a new Master directory.
        """
        path_to_excel = filedialog.askopenfilename()
        
        self.df = pd.read_excel(path_to_excel)
        
        for rows in self.df["Titolo"]:
            elaborated = truncate_path(rows)
            self.screen_path = os.path.join(self.path, f"Sanity/{elaborated}/Screenshots")
            os.makedirs(self.screen_path)
            self.doc_path = os.path.join(self.path, f"Sanity/{elaborated}/Master.docx")
            document = Document()
            document.add_heading(rows, 2)
            document.add_paragraph('ID=')
            document.save(self.doc_path)
        
        messagebox.showinfo(title="Cartella creata!", message="Cartella Sanity creata!")

# ------------------------------------------------------------------------------------------------------
# Needed: Error Handling, also trying to enable long paths on the folders.
# Enabling long path on the machine is not the solution. Truncating the path is seemingly doing nothing.

class DocxUpdater:
    """ 
    Copypastes images in order of creation from a 'Screenshots' folder onto a 'Master.docx' file, in a specified path.
    """
    def __init__(self, root_dir):
        """
        Initializes the class with the root directory containing the folders.
        """
        self.root_dir = root_dir

    def get_screenshot_folders(self):
        """
        Get all subfolders that contain a 'Screenshots' directory.
        """
        screenshot_folders = []
        for root, dirs, files in os.walk(self.root_dir):
            if 'Screenshots' in dirs and 'Master.docx' in files:
                screenshot_folders.append(root)
        return screenshot_folders

    def get_img_files(self, screenshots_folder):
        """
        Retrieves and sorts image files by creation time in the 'Screenshots' folder. The image files must be either .jpg or .png .
        """
        png_files = []
        screenshots_path = os.path.join(screenshots_folder, 'Screenshots')

        if os.path.isdir(screenshots_path):

            for file in os.listdir(screenshots_path):
                
                if format_checker(file, '.jpg','.png'):
                    png_path = os.path.join(screenshots_path, file)
                    creation_time = os.path.getctime(png_path)
                    png_files.append((file, creation_time))
        
        # Sort by creation time
        png_files.sort(key=lambda x: x[1])
        return [os.path.join(screenshots_path, file[0]) for file in png_files]

    def insert_images_to_docx(self, docx_path, png_files):
        """
        Inserts the sorted image files into the given .docx file.
        """
        doc = Document(docx_path)
        
        # Are width and height necessary??
        # Is the truncation needed here?
        for png_file in png_files:
            # Open the image
            img = Image.open(png_file)
            width, height = img.size
            # Insert image into the docx file
            doc.add_picture(png_file, width=Inches(5))
            doc.add_paragraph(f"\n")
        
        doc.save(docx_path)

    def process_folders(self):
        """
        Iterates over all folders and inserts the screenshots into the corresponding Master.docx files.
        """
        folders = self.get_screenshot_folders()
        
        # Needs testing! To understand what is necessary and what not.
        try:
            for folder in folders:
                docx_path = os.path.join(folder, 'Master.docx')
                # Checks rudimentally if the Master has images in it
                if os.path.getsize(docx_path) <= 36000:

                # Get the .png files sorted by creation time
                    png_files = self.get_img_files(folder)
                
                # Insert the .png files into the Example.docx file
                    self.insert_images_to_docx(docx_path, png_files)

            # Message to confirm the successful operation
            messagebox.showinfo(title="Success!", message="Smistamento riuscito! Controlla i file master!")
        except Exception as e:
            messagebox.showerror(title="Error", message= f"Something went wrong: {e}")
        




