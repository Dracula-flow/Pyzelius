# Qui legheremo la GUI alle classi
from src.Classes import CSV_File as csv, WorkTree as WT, Report 
from src.Functions import time_responser

class Controller:
    def __init__(self,root):
        self.root = root
        self.new_folder_path= None

    @staticmethod
    def new_daily_folder():
        # folder_path = r"D:\Users\Principale\Desktop\Report_Maker_v0.1"
        global new_folder_path
        new_folder = WT()
        new_folder.create_worktree()
        new_folder_path = getattr(new_folder, 'path')


    @staticmethod
    def new_defect_folder(entry):
        if new_folder_path is not None:
            dir_name = rf"{new_folder_path}/{time_responser('date')}/Defects/{entry}"
            WT.create_subdir(new_folder_path,dir_name)
        else:
            print("Error")

    
    # @classmethod
    def new_csv_files(self):
        Passed_file = csv("Passed")
        passed_headers = csv.passed_headers()
        passed_rows = csv.create_row(rf"{self.new_folder_path}\Passed")
        Passed_file.create_file(passed_headers,passed_rows)

        Defect_file = csv("Defects")
        defect_headers = csv.defect_headers()
        defect_rows = csv.create_row(rf"{self.new_folder_path}\Defects")
        Defect_file.create_file(defect_headers,defect_rows)

        self.new_report()

    # @classmethod
    def new_report(self):
        today_report = Report()
        today_report.data_feed()
