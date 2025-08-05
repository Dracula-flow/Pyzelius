from pathlib import Path
from typing import List, Optional, Dict

import pyperclip
from watchdog.observers import Observer

from src.Classes import DeviceUpdater, DocxUpdater, Pathfinder as PF, Signature as SI, WorkTree as WT, SanityTree as ST, CSV_File as CSV, Report, Archiver 
from src.Functions import time_responser

class Watcher:
    def __init__(self, path: Path):
        self.path = path
        self.observer: Optional[Observer] = None # type: ignore

    def start_watching(self, entry:object):
        template = entry.get().strip()
        event_handler = Archiver(template)

        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=False)
        self.observer.start()

    def stop_watching(self):
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        else:
            print("Error.")

class DeviceController:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.devices = DeviceUpdater(config_path)

    def load_devices(self, tree: object) -> None:
        """Load devices into given tree widget (GUI responsibility)."""
        self.devices.load_devices(tree)

    def get_devices(self) -> Dict[str, dict]:
        """Return devices dictionary from config."""
        import json
        with open(self.config_path, "r") as f:
            config_data = json.load(f)
        return config_data.get("Devices", {})

    def on_device_select(self, device_name: str) -> Optional[str]:
        """Return OS of selected device name or None if not found."""
        config_data = self.get_devices()
        for device_id, data in config_data.items():
            if data.get("device") == device_name:
                return data.get("os", None)
        return None

    def device_manager_commands(self, selector: str, id: str = "", device: str = "", os: str = "") -> None:
        """Add, modify, or delete device entry."""
        actions = {
            'add': lambda: self.devices.add_entry(device, os),
            'modify': lambda: self.devices.modify_entry(id, device, os),
            'delete': lambda: self.devices.delete_entry(id),
        }
        if selector not in actions:
            raise ValueError(f"Invalid selector '{selector}'. Use 'add', 'modify', or 'delete'.")
        actions[selector]()

class Controller:
    def __init__(
        self, 
        root: object,
        pathfinder: Optional[PF] = None,
        # signature: Optional[SI] = None,
        device_controller: Optional[DeviceController] = None,
        updater: Optional[DocxUpdater] = None,
    ):
        self.root = root
        self.pathfinder = pathfinder or PF()
        # self.signature = signature or SI()
        self.config = self.pathfinder.get_config_path()
        self.new_folder_path = self.pathfinder.get_path()
        self.updater = updater or DocxUpdater(Path(self.new_folder_path) / 'Sanity')
        self.device_controller = device_controller or DeviceController(self.config)
        self.watcher = Watcher(self.new_folder_path)
        self.date_str = time_responser('date')

    def on_copy(self, entry_values: List[str], signature:SI) -> None:
        """
        Combine entries via signature class and copy result to clipboard.
        Controller is agnostic of GUI widgets.
        """
        try:
            result = signature.entry_combine(entry_values)
            pyperclip.copy(result)
        except AttributeError:
            print("Error: signature.entry_combine failed.")

    def copy_text(self, text: str) -> None:
        """Copy given text string to clipboard."""
        pyperclip.copy(text)

    def update_path(self):
        """
        Update path if valid.
        Returns True if updated, False otherwise.
        """
        new_path = Path(self.pathfinder.modify_last_path())
        if new_path:
            self.new_folder_path = str(new_path)
            self.updater = DocxUpdater(new_path / 'Sanity')
            return True
        return False

    def get_device_os(self, device_name: str) -> Optional[str]:
        """Get OS for device by name."""
        return self.device_controller.on_device_select(device_name)

    def device_manager_commands(self, selector: str, id: str = "", device: str = "", os: str = "") -> None:
        """Proxy to device controller."""
        self.device_controller.device_manager_commands(selector, id, device, os)

    def start_watching(self, entry, label:object):
        "Proxy to watcher"
        self.watcher.start_watching(entry)
        label.config(text= "RENAMER: ON")

    def stop_watching(self, label:object):
        self.watcher.stop_watching()
        label.config(text= "RENAMER: OFF")

    def new_daily_folder(self):
        """Creates instance of WorkTree and corresponding folder"""
        new_folder = WT(self.new_folder_path)
        new_folder.create_worktree()

    def new_sanity_folder(self):
        """Creates instance of SanityTree and corresponding folder"""
        new_folder = ST(self.new_folder_path)
        new_folder.new_master_dir()

    def sanity_paste(self):
        self.updater.process_folders()

    def new_report(self):
        
        daily_folder = Path(self.new_folder_path)/self.date_str

        Passed_data = CSV("Passed", daily_folder)
        Defect_data = CSV("Defects", daily_folder)
       
        df_passed= Passed_data.to_dataframe(daily_folder, CSV.passed_headers())
        df_defect= Defect_data.to_dataframe(daily_folder, CSV.defect_headers())

        today_report = Report(daily_folder/"Report")
        today_report.data_feed(df_passed, df_defect)