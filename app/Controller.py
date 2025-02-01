# Qui legheremo la GUI alle classi
from src.Classes import CSV_File as csv, WorkTree as WT, Report, Pathfinder as PF 
from src.Functions import time_responser

class Controller:
    def __init__(self,root):
        self.root = root
        self.new_folder_path= None 
        self.date_str = time_responser('date')
        self.pathfinder = PF()

    # @staticmethod
    def new_daily_folder(self):
        # folder_path = r"D:\Users\Principale\Desktop\Report_Maker_v0.1"
        self.new_folder_path = self.pathfinder.get_path()

        new_folder = WT(self.new_folder_path)
        new_folder.create_worktree()

    def new_path_folder(self):
        self.new_folder_path = self.pathfinder.modify_last_path()


    # @staticmethod
    def new_defect_folder(self,entry):

        if self.new_folder_path is not None:
            dir_name = rf"{self.new_folder_path}/{self.date_str}/Defects/{entry}"
            WT.create_subdir(self.new_folder_path,dir_name)
        else:
            print("Error")

    
    # @staticmethod
    def new_report(self):

        Passed_file = csv("Passed")
        passed_headers = csv.passed_headers()
        passed_rows = csv.create_row(rf"{self.new_folder_path}/{self.date_str}/Passed")
        Passed_file.create_file(passed_headers,passed_rows)

        Defect_file = csv("Defects")
        defect_headers = csv.defect_headers()
        defect_rows = csv.create_row(rf"{self.new_folder_path}/{self.date_str}/Defects")
        Defect_file.create_file(defect_headers,defect_rows)

        today_report = Report()
        today_report.data_feed()
