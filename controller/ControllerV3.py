

from pathlib import Path
from typing import Optional, List

from src import Pathfinder as PF, Worktree as WT
from src.Functions import time_responser

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
        self.base_path = self.pathfinder.get_path()
        self.date_str = time_responser('date')

        self.device_controller = DeviceController(self.config_path)
        self.signature_controller = SignatureController()
        self.report_controller = ReportController(self.base_path, self.date_str)
        self.sanity_controller= SanityController(self.base_path)
        self.watcher_controller = WatcherController(self.base_path)


    #----------------- Device Controller Actions-------------------------

    def get_device_os(self, device_name: str) -> Optional[str]:
        return self.device_controller.on_device_select(device_name)

    def device_command(self, action: str, id: str = "", device: str = "", os: str = "") -> None:
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
        self.watcher_controller.start(entry_widget)
        label_widget.config(text="RENAMER: ON")

    def stop_watching(self, label_widget: object) -> None:
        self.watcher_controller.stop()
        label_widget.config(text="RENAMER: OFF")

    # ---------------------------Base Path Update-----------------------------

    def update_path(self):
        """
        Update path if valid.
        Returns True if updated, False otherwise.
        """
        new_path = Path(self.pathfinder.modify_last_path())
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
