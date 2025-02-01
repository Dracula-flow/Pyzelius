from datetime import datetime as dt
from tkinter import filedialog
from pathlib import Path
import os, json

root_dir = Path(__file__).resolve().parent.parent

# A function to return different time components in the form of a formatted string, based on the input parameter
def time_responser(selector):
    date = dt.now().strftime('%d-%m-%Y')
    time = dt.now().strftime('%H:%M')

    output={
        'date' : date,
        'time' : time,
        'datetime' : f"{date} {time}"
    }

    try:
        return output.get(selector)
    except: 
        if selector not in output:
            raise ValueError(f"Error: {selector} is NOT a valid parameter. Time_responser only takes 'date', 'time' and 'datetime' as parameters")
        



# PROBLEMA: se non c'è un file config in /config, il programma apre direttamente una finestra di dialogo per la scelta, senza spiegazioni.
# Sta cosa va risolta... 
# Risolto: si chiamava la funzione get_path una volta di troppo dal Controller. Ora va bene. Resta da fare in modo che una cartella possa essere selezionata come repo...
# Risolto: costruita funziona ad hoc. Inserita variabile "globale" per semplificare la scrittura
def get_path():
    # Get the directory path using filedialog.askdirectory(), with a fallback to last used path.
    root_path = load_last_path()  # Try loading the last path first
    if not root_path:
        root_path = filedialog.askdirectory()  # If no last path, ask the user for a new one

    if root_path:  # Only save if a valid path is selected
        save_last_path(root_path)

    return root_path
        
def load_last_path():
    # Load the last used directory path from a configuration file.
    if os.path.exists(rf"{root_dir}/config/config.json"):
        with open(rf"{root_dir}/config/config.json", 'r') as config_file:
            config = json.load(config_file)
            return config.get("last_path", "")
    return ""  # Return an empty string if no path was saved

def save_last_path(path):
    # Save the current directory path to the configuration file.
    config = {"last_path": path}
    with open(rf"{root_dir}/config/config.json", 'w') as config_file:
        json.dump(config, config_file)

def modify_last_path():
    # Chiedi all'utente di selezionare una nuova directory
    new_path = filedialog.askdirectory()

    if new_path:  # Se l'utente ha selezionato un percorso
        # Carica il file di configurazione esistente
        config_file_path = rf"{root_dir}/config/config.json"
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as config_file:
                config = json.load(config_file)
            
            # Modifica il percorso dell'ultima directory
            config["last_path"] = new_path
            
            # Salva il file con il nuovo percorso senza rimuovere gli altri dati
            with open(config_file_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)

        else:
            print(f"Il file di configurazione non esiste: {config_file_path}")