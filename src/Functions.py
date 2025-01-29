from datetime import datetime as dt
from tkinter import filedialog
import os, json

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
        
# A function to ideally assemble the path to every folder the program needs
# def get_path():
#     root_path = filedialog.askdirectory()
#     return root_path

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
    if os.path.exists(rf"C:\Users\Simone Avagliano\Desktop\Pyzelius-main\Pyzelius-main\config\config.json"):
        with open(rf"C:\Users\Simone Avagliano\Desktop\Pyzelius-main\Pyzelius-main\config\config.json", 'r') as config_file:
            config = json.load(config_file)
            return config.get("last_path", "")
    return ""  # Return an empty string if no path was saved

def save_last_path(path):
    # Save the current directory path to the configuration file.
    config = {"last_path": path}
    with open(rf"C:\Users\Simone Avagliano\Desktop\Pyzelius-main\Pyzelius-main\config\config.json", 'w') as config_file:
        json.dump(config, config_file)