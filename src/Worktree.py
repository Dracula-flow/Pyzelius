from pathlib import Path
from tkinter import messagebox

from .Functions import time_responser

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
        root_path = Path(self.path)/self.dirname
        try:
            Path.mkdir(root_path)
            messagebox.showinfo(title="Cartella creata!", message=f"Cartella {self.dirname} creata!")
        except FileExistsError:
            messagebox.showerror(title="Errore!",message=f"La cartella {self.dirname} esiste già nella destinazione!")

        for subdir in self.subdirs:
            subdir_path = root_path/subdir
            Path.mkdir(subdir_path)