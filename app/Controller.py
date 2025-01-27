# Qui legheremo la GUI alle classi
from src.Classes import CSV_File as csv, WorkTree as WT, Report 

class Controller:
    def __init__(self,root):
        self.root = root

    @staticmethod
    def new_daily_folder():
        folder_path = r"D:\Users\Principale\Desktop\Report_Maker_v0.1"
        new_folder = WT(folder_path)
        new_folder.create_worktree()

    @staticmethod
    def new_defect_folder(path,dir_name):
        WT.create_subdir(path,dir_name)

    
    @classmethod
    def new_csv_files(cls):
        Passed_file = csv("Passed")
        passed_headers = csv.passed_headers()
        passed_rows = csv.create_row(r"D:\Users\Principale\Desktop\Report_Maker_v0.1\date-today\Passed")
        Passed_file.create_file(passed_headers,passed_rows)

        Defect_file = csv("Defects")
        defect_headers = csv.defect_headers()
        defect_rows = csv.create_row(r"D:\Users\Principale\Desktop\Report_Maker_v0.1\date-today\Defects")
        Defect_file.create_file(defect_headers,defect_rows)

        cls.new_report()

    @classmethod
    def new_report(cls):
        today_report = Report()
        today_report.data_feed()