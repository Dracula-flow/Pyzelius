import json,sys
from pathlib import Path
from tkinter import filedialog

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
            config_folder = Path.home()/'pyzelius_config'
            if not Path.exists(config_folder):
                config_folder.mkdir(parents=True, exist_ok=False)
            config_path = config_folder/"config.json"

            if not config_path.exists():
                default_config = {}  # or provide a meaningful default structure
                with config_path.open('w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4)
            return config_path
            
        else:
            # If running as a Python script, use the relative path
            return Path(__file__).resolve().parent.parent / 'config/config.json'
        
    def load_last_path(self):
        """
        Load the last used directory path from a configuration file.
        """
        if Path.exists(self.config_last_path):
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
        
        from tkinter import messagebox

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
            return new_path
        return None
    
    def get_path(self):
        return self.last_path