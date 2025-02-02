import os
from src.Classes import CSV_File as csv, WorkTree as WT, Report, Pathfinder as PF, Signature as SI
from src.Functions import time_responser

# This class handles the business logic between the Classes in src and the GUI in app.
class Controller:
    def __init__(self,root):

        self.root = root
        self.pathfinder = PF()
        self.new_folder_path= self.pathfinder.get_path() 
        self.date_str = time_responser('date')

    def new_daily_folder(self):

        new_folder = WT(self.new_folder_path)
        new_folder.create_worktree()

    def new_path_folder(self):

        self.new_folder_path = self.pathfinder.modify_last_path()

    def new_defect_folder(self,entry):

        if self.new_folder_path is not None:
            
            dir_name = rf"{self.new_folder_path}/{self.date_str}/Defects/{entry}"
            WT.create_subdir(self.new_folder_path,dir_name)
        else:
            print("Error")

    def new_report(self):
        
        daily_folder = os.path.join(self.new_folder_path,self.date_str)

        Passed_file = csv("Passed", daily_folder)
        passed_headers = csv.passed_headers()
        passed_rows = Passed_file.create_row(daily_folder)
        Passed_file.create_file(passed_headers,passed_rows)

        Defect_file = csv("Defects", daily_folder)
        defect_headers = csv.defect_headers()
        defect_rows = Defect_file.create_row(daily_folder)
        Defect_file.create_file(defect_headers,defect_rows)

        today_report = Report(rf"{daily_folder}/Report")
        today_report.data_feed()
        today_report.delete_csv(Passed_file.filename,Defect_file.filename)
