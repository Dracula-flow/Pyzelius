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
        assert self.dirname is not None, "Directory name cannot be None"
        root_path = Path(self.path)/self.dirname
        try:
            Path.mkdir(root_path)
            messagebox.showinfo(
                title=_("Folder created!"), # type: ignore - it's a builtin, check Localization.py
                message=_("Folder {name} created!").format(name=self.dirname) # type: ignore - it's a builtin, check Localization.py
            )
        except FileExistsError:
            messagebox.showerror(
                title=_("Error!"), #type: ignore - it's a builtin, check Localization.py
                message=_("Folder {name} already exists at destination!").format(name=self.dirname) #type: ignore - it's a builtin, check Localization.py
            )

        for subdir in self.subdirs:
            subdir_path = root_path/subdir
            Path.mkdir(subdir_path)