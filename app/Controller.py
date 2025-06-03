import pyperclip,json
import tkinter as tk
from pathlib import Path
from src.Classes import CSV_File as csv, WorkTree as WT, Report, Pathfinder as PF, Master, Signature as SI, DocxUpdater, DeviceUpdater
from src.Functions import time_responser

# This class handles the business logic between the Classes in src and the GUI in app.
class Controller:
    def __init__(self,root):

        self.root = root
        self.pathfinder = PF()
        self.signature = SI()
        self.config = self.pathfinder.get_config_path()
        self.new_folder_path= self.pathfinder.get_path() 
        self.updater = DocxUpdater(Path(self.new_folder_path)/'Sanity')
        self.devices = DeviceUpdater(self.config)
        self.date_str = time_responser('date')

    def new_daily_folder(self):

        new_folder = WT(self.new_folder_path)
        new_folder.create_worktree()

    def new_path_folder(self):

        self.new_folder_path = self.pathfinder.modify_last_path()

    def new_report(self):
        
        daily_folder = Path(self.new_folder_path)/self.date_str

        Passed_data = csv("Passed", daily_folder)
        Defect_data = csv("Defects", daily_folder)
       
        df_passed= Passed_data.to_dataframe(daily_folder, csv.passed_headers())
        df_defect= Defect_data.to_dataframe(daily_folder, csv.defect_headers())

        today_report = Report(daily_folder/"Report")
        today_report.data_feed(df_passed, df_defect)

    def new_sanity_folder(self):
        new_folder = Master(self.new_folder_path)
        new_folder.new_master_dir()

    def on_copy(self,entry_list,signature_class):

        try:
            entry_values = [entry.get() for entry in entry_list]
            result = signature_class.entry_combine(entry_values)

            pyperclip.copy(result)
        except AttributeError:
            pass
    
    def copy_text(self, entryField):
        # Get the content from the Text widget
        note_content = entryField.get("1.0", tk.END).strip()
        
        # Use pyperclip to copy the content to the clipboard
        pyperclip.copy(note_content)


    def sanity_paste(self):
        self.updater.process_folders()

    def device_getter(self):
        with open (self.config, "r") as f:
            config_data = json.load(f)
            return config_data.get("Devices",{})
        
    def on_device_select(self, event, combobox, config_data, os_entry):
        device_name = combobox.get()  # Get the selected device name

        # Find the corresponding device ID using the name (invert the mapping)
        device_id = None
        for key, value in config_data.items():
            if value["device"] == device_name:
                device_id = key
                break
    
        if device_id and device_id in config_data:
            os = config_data[device_id].get("os", "")  # Get the OS for the selected device ID
            os_entry.delete(0, tk.END)  # Clear the current OS value
            os_entry.insert(0, os)  # Insert the OS value for the selected device

    def device_manager_commands(self,selector:str,id:str="",device:str="",os:str=""):
        
        actions={
        'add' : lambda: self.devices.add_entry(device,os),
        'modify' : lambda: self.devices.modify_entry(id,device,os),
        'delete' : lambda: self.devices.delete_entry(id)
        }

        if selector not in actions:
            raise ValueError(f"Error: {selector} is NOT a valid parameter. Device_manager_commands only takes 'add', 'modify' and 'delete' as parameters")

        return actions[selector]()
    
    def device_manager_load(self,tree:object):
        self.devices.load_devices(tree)
       