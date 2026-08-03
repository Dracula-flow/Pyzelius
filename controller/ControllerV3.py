

import os
import sys
import subprocess

from pathlib import Path
from typing import Optional, List

from src import Pathfinder as PF, WorkTree as WT
from src.Functions import time_responser
from src.Localization import Localization

from .DeviceController import DeviceController
from .ReportController import ReportController
from .SignatureController import SignatureController
from .WatcherController import WatcherController
from .SanityController import SanityController

import pyperclip

class ControllerV3:
    """
    High-level application controller that delegates responsibilities
    to specialized controllers: device, signature, report, and watcher.
    """
    def __init__(self, root: object, pathfinder: Optional[PF] = None):

        self.root = root
        self.pathfinder = pathfinder or PF()

        self.config_path = self.pathfinder.get_config_path()
        self.base_path = Path(self.pathfinder.get_path())
        self.date_str = time_responser('date')

        self.device_controller = DeviceController(self.config_path)
        self.signature_controller = SignatureController()
        self.report_controller = ReportController(self.base_path, self.date_str)
        self.sanity_controller= SanityController(self.base_path)
        self.watcher_controller = WatcherController(self.base_path)


    #----------------- Device Controller Actions-------------------------

    def get_device_os(self, device_name: str) -> Optional[str]:
        return self.device_controller.on_device_select(device_name)

    def device_command(self, action: str, id: int = 0, device: str = "", os: str = "") -> None:
        self.device_controller.device_manager_commands(action, id, device, os)

    def get_device_config(self) -> dict:
        return self.device_controller.get_devices()
    
    #----------------------Signature Controller Actions---------------------

    def on_copy_signature(self, entry_values: List[str], mode: str = "Full") -> None:
        """
        Generate a signature string for the given mode and copy it to clipboard.
        """
        try:
            signature_controller = SignatureController(mode)
            signature_controller.copy_to_clipboard(entry_values)
        except Exception as e:
            print(f"Error generating or copying signature: {e}")

    def get_signature_fields(self, mode: str = "Full") -> List[str]:
        """
        Return the input field labels for the selected signature mode.
         Useful for building dynamic entry fields in the GUI.
        """
        controller = SignatureController(mode)
        return controller.get_fields()
    
    #--------------------- Report Generation -------------------------------

    def generate_report(self)-> None:
        self.report_controller.generate_report()
    
    #---------------------- Folder Watching --------------------------------

    def start_watching(self, entry_widget: object, label_widget: object) -> None:
        self.watcher_controller.start_watching(entry_widget)
        label_widget.config(text=_("Renamer: ON")) # type: ignore - the object is passed to it via arguments, and it is a Label widget from tkinter.ttk

    def stop_watching(self, label_widget: object) -> None:
        self.watcher_controller.stop_watching()
        label_widget.config(text=_("Renamer: OFF")) # type: ignore - the object is passed to it via arguments, and it is a Label widget from tkinter.ttk

    # ---------------------------Base Path Update-----------------------------

    def update_path(self):
        """
        Update path if valid.
        Returns True if updated, False otherwise.
        """
        new_path = self.pathfinder.modify_last_path()
        if new_path:
            self.base_path = str(new_path)
            return True
        return False

    # ----------------------New Worktree Creation----------------------------

    def new_daily_folder(self):
        """
        Creates instance of WorkTree and corresponding folder
        """
        WT(self.base_path).create_worktree()

    # ----------------------Copypaste from NotePanel--------------------------

    def copy_text(self, text: str) -> None:
        """Copy given text string to clipboard."""
        pyperclip.copy(text)


    #-----------------------Sanity Folders processing------------------------


    def new_sanity_folder(self):
        """
        Creates instance of SanityTree and corresponding folder
        """
        self.sanity_controller.create_sanity_tree()
        

    def sanity_paste(self):
        """
        Copypastes the Sanity screenshots in chronological order on the corresponding Master.docx files.
        """
        self.sanity_controller.process_screen_folders()

    #-----------------------Language selection--------------------------------

    def change_language(self, lang_code: str) -> None:
        """
        Persists the chosen language and restarts the app so every widget
        gets rebuilt with the new translations (Tkinter widgets don't
        retranslate themselves live).
        """
        Localization.set_language(lang_code, self.config_path)
        self.restart_app()

    def restart_app(self) -> None:
        """
        Closes the current window and relaunches the whole process,
        so the app comes back up fully translated.
        """
        if hasattr(self.root, "destroy"):
            try:
                self.root.destroy() #type:ignore - the object is passed to it via arguments, and it is a Tkinter root window
            except Exception:
                pass

        # Use subprocess to spawn a new Python process instead of os.execv.
        # This avoids Windows/PowerShell quoting/path issues when paths contain spaces.
        try:
            cmd = [sys.executable] + list(sys.argv)
            # Ensure script path (argv[1]) is absolute when present
            if len(cmd) > 1 and not os.path.isabs(cmd[1]):
                cmd[1] = os.path.abspath(cmd[1])
            subprocess.Popen(cmd)
        finally:
            # Exit the current process regardless of spawn result
            sys.exit(0)
