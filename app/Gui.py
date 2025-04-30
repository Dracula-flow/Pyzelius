# Qui creeremo la classe per la GUI usando Tkintr

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.Controller import Controller as CT
from src.Classes import Signature, SignatureSanity, SignatureMinimal
from src.Functions import apply_char_limit


class SignaturePanel(tk.Frame):
    """
    Houses the 3 different signature types.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.controller =  CT(self)
        self.create_widgets()
        
    def create_widgets(self):
        tabControl = ttk.Notebook(self)
        
        signature = Signature()
        signature_sanity = SignatureSanity()
        signature_minimal = SignatureMinimal()
        
        tabs = (
                ("Full", signature), 
                ("Sanity", signature_sanity), 
                ("Simple", signature_minimal)
                )
        
        config_data = self.controller.device_getter()

        for tab_name, signature_class in tabs:
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=f"{tab_name}")

            entry_list = []

            for i, field in enumerate(signature_class.input_fields):
                ttk.Label(tab, text=field).grid(row=i, column=0, padx=10, pady=5)

                if field == "Puntamento":
                    entry = ttk.Combobox(tab, values=("Application","Performance","Post Release","System","User Acceptance"), state="readonly")
                    entry.current(None)
                elif field == "DEVICE":
                    # The Device and OS fields are linked, the data is provided via config.json
                    device_names = [device_info["device"] for device_info in config_data.values()]
                    entry = ttk.Combobox(tab,values=device_names)
                    entry.current(None)
                    entry.bind("<<ComboboxSelected>>", lambda event, entry=entry: self.controller.on_device_select(event, entry, config_data, os_entry))
                elif field == "OS":
                    os_entry = ttk.Entry(tab)
                    os_entry.grid(row=i, column=1, padx=10, pady=5)
                    apply_char_limit(os_entry, 50)
                    entry_list.append(os_entry)  # Add the OS entry to the list
                    continue  # Skip adding this entry to the list later, since we already added it here
                else:
                    entry = ttk.Entry(tab)
                    apply_char_limit(entry,50)

                entry.grid(row=i, column=1, padx=10, pady=5)
                entry_list.append(entry)

                button = ttk.Button(tab, text="Copia firma (Alt+D)", command=lambda entry_list=entry_list, signature_class=signature_class: self.controller.on_copy(entry_list, signature_class))
                button.grid(row=len(signature_class.input_fields), column=0, columnspan=2, pady=20)


            # def bind_hotkey(event, entry_list=entry_list, signature_class=signature_class):
            #     self.controller.on_copy(entry_list, signature_class)

            # tab.bind("<Alt-d>", bind_hotkey)  # Use `tab` as the target for the hotkey binding

            tab.bind("<Alt-d>", lambda event: self.controller.on_copy(entry_list,signature_class))

            
        tabControl.pack(expand = 1, fill ="both") 


class NotePanel(tk.Frame):
    """
    A simple text panel to store notes, and a button to copy them to the clipboard.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.controller =  CT(self)
        self.create_widgets()
    
    def create_widgets(self):
        noteFrame = tk.Frame(self)
        noteFrame.pack(padx=10,pady=10)
        entryField = tk.Text(noteFrame, height=8, width=30)
        entryField.pack(padx=5, pady=5)

        button = ttk.Button(noteFrame, text="Copia nota (Alt+F)", command=lambda: self.controller.copy_text(entryField))
        button.pack(pady=5)

        self.master.bind("<Alt-f>", lambda event: self.controller.copy_text(entryField))

class DeviceManagerWindow(tk.Toplevel):
    """
    UI to host the Treeview displaying the devices registered on the JSON
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.controller= CT(self)
    
        self.title("Device Manager")
        self.geometry("625x300")

          # Create the Treeview widget
        columns=("ID","Device","OS")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Add buttons to modify, add, and delete entries
        self.add_button = tk.Button(self, text="Add Device",command= lambda: self.show_device_popup('add'))
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        self.modify_button = tk.Button(self, text="Modify Device",command= lambda: self.show_device_popup('mod'))
        self.modify_button.grid(row=1, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self, text="Delete Device", command= self.delete_selected_device)
        self.delete_button.grid(row=1, column=2, padx=10, pady=10)

        self.controller.device_manager_load(self.tree)

    def refresh_treeview(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Reload from JSON
        self.controller.device_manager_load(self.tree)

    #Something wrong in the interaction between the two sets of functions.
    # SOlution: parenthesis. Opup windows need to be called when the button is pressed and not immediately
    def show_device_popup(self, action: str, device_id=None, current_device="", current_os=""):
        controller = CT(self)
        popup = tk.Toplevel(self)

    # Dynamic title based on action
        title = "Add Device" if action == "add" else "Modify Device"
        popup.title(title)
        popup.geometry("300x200")
        popup.transient(self)
        popup.grab_set()
        
    # Labels and entries
        tk.Label(popup, text="Device:").grid(row=0,column=1, pady=2,sticky='ew')
        device_entry = tk.Entry(popup)
        device_entry.grid(row=0, column=2, pady=2, sticky="ew")
        device_entry.insert(0, current_device)

        tk.Label(popup, text="OS:").grid(row=1,column=1, pady=2, sticky="ew")
        os_entry = tk.Entry(popup)
        os_entry.grid(row=1,column=2,pady=2, sticky="ew")
        os_entry.insert(0, current_os)

        def on_submit():
            device_name = device_entry.get()
            os_version = os_entry.get()

            if device_name and os_version:
                if action == "add":
                    controller.device_manager_commands("add", device=device_name, os=os_version)
                elif action == "mod" and device_id is not None:
                    controller.device_manager_commands("modify", id=str(device_id), device=device_name, os=os_version)
                else:
                    messagebox.showerror("Error", "Invalid action or missing ID.")
                    return

                self.refresh_treeview()
                popup.destroy()
            else:
                messagebox.showwarning("Input Error", "Both fields must be filled!")

        action_label = "Add" if action == "add" else "Modify"
        submit_btn = tk.Button(popup, text=action_label, command=on_submit)
        submit_btn.grid(row=2, column=2, columnspan=2, pady=2, sticky="ew")
        

    def delete_selected_device(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a device to delete.")
            return

        values = self.tree.item(selected_item, 'values')
        device_id = values[0]
        device_name = values[1]

            # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete device '{device_name}' (ID: {device_id})?")
        if confirm:
            controller = CT(self)
            try:
                controller.device_manager_commands("delete", id=str(device_id))
                self.refresh_treeview()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pyzelius v1.6.0")
        self.geometry("360x580")

        self.controller = CT(self)
        self.create_menu()
        self.create_widgets()

    def create_menu(self):

        menu_bar= tk.Menu(self)

        menu_structure = {
            "Nuovo..." : [("Cartella giornaliera", self.controller.new_daily_folder),
                          ("Cartella Sanity", self.controller.new_sanity_folder),
                            ("Report", self.controller.new_report)],
            "Azioni..." : [("Modifica path", self.controller.new_path_folder),
                           ("Smista screen Sanity", self.controller.sanity_paste),
                           ("Device Manager", self.open_device_manager)
                           ],
        }

        for label,command in menu_structure.items():
            menu = self.create_submenu(menu_bar, command)
            menu_bar.add_cascade(label=label, menu=menu)

        self.config(menu=menu_bar)

    def create_submenu(self, parent_menu, items):
        """Helper method to create a submenu with commands."""
       
        submenu = tk.Menu(parent_menu, tearoff=0)
       
        for label, command in items:
           
            submenu.add_command(label=label, command=command)
            submenu.add_separator()  # Add separator between items
        return submenu
    
    def open_device_manager(self):
        """Method to open the DeviceManagerWindow."""
        DeviceManagerWindow(self)  # Create and open the device manager window

    def create_widgets(self):
        sign_panel= SignaturePanel(master=self)
        note_panel= NotePanel(master=self)
        sign_panel.pack(padx=10, pady=10)
        note_panel.pack(padx=10,pady=10)
