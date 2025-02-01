from tkinter import filedialog
from pathlib import Path
import os, json

class Pathfinder:
    def __init__(self, config_last_path):
        self.config_last_path = config_last_path
        self.last_path = self.load_last_path()

    def load_last_path(self):
        # Load the last used directory path from a configuration file.
        if os.path.exists(self.config_last_path):
            with open(self.config_last_path, 'r') as config_file:
                config = json.load(config_file)
                return config.get("last_path", "")
        return ""  # Return an empty string if no path was saved

    def save_last_path(self):
        # Save the current directory path to the configuration file.
        config = {"last_path": self.last_path}
        with open(self.config_last_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

    def modify_last_path(self):
        # Chiedi all'utente di selezionare una nuova directory
        new_path = filedialog.askdirectory()

        if new_path:  # Se l'utente ha selezionato un percorso
            # Carica il file di configurazione esistente
            self.last_path = new_path
            self.save_last_path()

    def get_path(self):
        return self.last_path