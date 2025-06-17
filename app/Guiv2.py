import tkinter as tk
from tkinter import ttk, messagebox
from app.Controllerv2 import Controller as CT
from src.Classes import Signature, SignatureSanity, SignatureMinimal
from src.Functions import apply_char_limit

class WatcherPanel(tk.Frame):
    """
    A tab to house the Watcher/Auto-renamer
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Renamer template:").grid(row=0, column=1)
        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=1, pady=5)
        self.status_label = ttk.Label(self, text="Renamer: OFF")
        self.status_label.grid(row=2,column=1)

        self.start_button = ttk.Button(self, text="Start", command=lambda: self.controller.start_watching(self.entry, self.status_label))
        self.start_button.grid(row=3,column=1,pady=5)

        self.stop_button = ttk.Button(self, text="Stop", command=lambda: self.controller.stop_watching(self.status_label))
        self.stop_button.grid(row=4, column=1,pady=5)



class SignatureTab(ttk.Frame):
    """
    A single tab within the SignaturePanel.
    """
    def __init__(self, parent, signature_class, config_data, controller):
        super().__init__(parent)
        self.signature_class = signature_class
        self.controller = controller
        self.config_data = config_data
        self.entry_list = []
        self.os_entry = None

        self.build_fields()
        self.build_button()

    def build_fields(self):
        for i, field in enumerate(self.signature_class.input_fields):
            ttk.Label(self, text=field).grid(row=i, column=0, padx=10, pady=5)

            entry = self.get_field_widget(field, i)
            entry.grid(row=i, column=1, padx=10, pady=5)

            if field != "OS":
                self.entry_list.append(entry)

    def get_field_widget(self, field, row):
        if field == "Puntamento":
            entry = ttk.Combobox(self, values=("Application", "Performance", "Post Release", "System", "User Acceptance"), state="readonly")
            entry.current(None)
        elif field == "DEVICE":
            device_names = [d["device"] for d in self.config_data.values()]
            entry = ttk.Combobox(self, values=device_names)
            entry.current(None)
            entry.bind("<<ComboboxSelected>>", lambda e: self.on_device_selected(entry))
        elif field == "OS":
            self.os_entry = ttk.Entry(self)
            apply_char_limit(self.os_entry, 50)
            return self.os_entry
        else:
            entry = ttk.Entry(self)
            apply_char_limit(entry, 50)
        return entry

    def on_device_selected(self, device_entry):
        selected_device = device_entry.get()
        os_value = self.controller.get_device_os(selected_device)
        if self.os_entry:
            self.os_entry.delete(0, tk.END)
            self.os_entry.insert(0, os_value or "")

    def build_button(self):
        btn = ttk.Button(self, text="Copia firma", command=self.on_copy)
        btn.grid(row=len(self.signature_class.input_fields), column=0, columnspan=2, pady=20)

    def on_copy(self):
        values = [e.get() for e in self.entry_list]
        if self.os_entry:
            values.insert(self.signature_class.input_fields.index("OS"), self.os_entry.get())
        self.controller.on_copy(values)


class SignaturePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)
        self.config_data = self.controller.device_controller.get_devices()
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        signature_types = [
            ("Full", Signature()),
            ("Sanity", SignatureSanity()),
            ("Simple", SignatureMinimal())
        ]

        for name, sig in signature_types:
            tab = SignatureTab(tab_control, sig, self.config_data, self.controller)
            tab_control.add(tab, text=name)
            tab.bind("<Alt-d>", lambda e: tab.on_copy())

        tab_control.pack(expand=1, fill="none")


class NotePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)
        self.create_widgets()
        
    def create_widgets(self):
        note_frame = tk.Frame(self)
        note_frame.pack(padx=10, pady=10)
        
        self.text_widget = tk.Text(note_frame, height=8, width=25, relief="solid")
        self.text_widget.pack(fill="both", expand=1)

        btn = ttk.Button(note_frame, text="Copia nota (Alt+F)", command=self.copy_note)
        btn.pack(pady=5)

        self.master.bind("<Alt-f>", lambda e: self.copy_note())

    def copy_note(self):
        self.controller.copy_text(self.text_widget.get("1.0", tk.END).strip())


class DeviceManagerWindow(tk.Toplevel):
    """
    Window that manages devices with a Treeview and CRUD controls.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Device Manager")
        self.geometry("625x300")
        self.controller = CT(self)

        self.columns = ("ID", "Device", "OS")
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons
        btn_cfg = [
            ("Add Device", self.open_add_popup),
            ("Modify Device", self.open_modify_popup),
            ("Delete Device", self.delete_selected_device)
        ]

        for col_index, (label, command) in enumerate(btn_cfg):
            btn = tk.Button(self, text=label, command=command)
            btn.grid(row=1, column=col_index, padx=10, pady=10)

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.controller.device_controller.load_devices(self.tree)

    def open_add_popup(self):
        DevicePopup(self, self.controller, action="add", on_close=self.populate_tree)

    def open_modify_popup(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a device to modify.")
            return

        values = self.tree.item(selected_item, "values")
        device_id, device_name, os_version = values
        DevicePopup(
            self, 
            self.controller,
            action="modify",
            device_id=device_id,
            device_name=device_name,
            os_version=os_version,
            on_close=self.populate_tree
        )

    def delete_selected_device(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a device to delete.")
            return

        device_id, device_name, _ = self.tree.item(selected_item, "values")
        confirm = messagebox.askyesno("Confirm Delete", f"Delete device '{device_name}' (ID: {device_id})?")
        if confirm:
            try:
                self.controller.device_manager_commands("delete", id=str(device_id))
                self.populate_tree()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

class DevicePopup(tk.Toplevel):
    """
    Popup window for adding or modifying a device.
    """
    def __init__(self, parent, controller, action, device_id=None, device_name="", os_version="", on_close=None):
        super().__init__(parent)
        self.controller = controller
        self.action = action
        self.device_id = device_id
        self.on_close = on_close

        self.title("Add Device" if action == "add" else "Modify Device")
        self.geometry("300x200")
        self.transient(parent)
        self.grab_set()

        self.device_entry = None
        self.os_entry = None

        self.create_widgets(device_name, os_version)

    def create_widgets(self, device_name, os_version):
        tk.Label(self, text="Device:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.device_entry = tk.Entry(self)
        self.device_entry.grid(row=0, column=1, padx=10, pady=5)
        self.device_entry.insert(0, device_name)

        tk.Label(self, text="OS:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.os_entry = tk.Entry(self)
        self.os_entry.grid(row=1, column=1, padx=10, pady=5)
        self.os_entry.insert(0, os_version)

        btn_label = "Add" if self.action == "add" else "Modify"
        submit_btn = tk.Button(self, text=btn_label, command=self.submit)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

    def submit(self):
        device_name = self.device_entry.get().strip()
        os_version = self.os_entry.get().strip()

        if not device_name or not os_version:
            messagebox.showwarning("Input Error", "Both fields must be filled!")
            return

        try:
            if self.action == "add":
                self.controller.device_manager_commands("add", device=device_name, os=os_version)
            elif self.action == "modify":
                self.controller.device_manager_commands("modify", id=self.device_id, device=device_name, os=os_version)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            if self.on_close:
                self.on_close()
            self.destroy() 

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pyzelius v1.8.0")
        self.geometry("360x650")

        self.controller = CT(self)

        self.configure_styles()
        self.create_menu()
        self.create_layout()

    def configure_styles(self):
        """
        Central place to manage ttk styles for consistent theming.
        """
        style = ttk.Style(self)
        style.theme_use("vista")  # Try 'clam', 'default', 'alt', or 'vista'

        style.configure("TButton",
                        font=("Arial", 10),
                        padding=6)

        style.configure("TLabel",
                        font=("Arial", 10),
                        padding=4)

        style.configure("TCombobox",
                        font=("Arial", 10),
                        padding=4)

        style.configure("TNotebook",
                        tabposition='n')  # Tabs on top

        style.configure("TNotebook.Tab",
                        font=("Arial", 10, "bold"),
                        padding=[10, 5])

    def create_menu(self):
        """
        Set up the menu bar with nested commands.
        """
        menu_bar = tk.Menu(self)

        menu_structure = {
            "Nuovo...": [
                ("Cartella giornaliera", self.controller.new_daily_folder),
                ("Cartella Sanity", self.controller.new_sanity_folder),
                ("Report", self.controller.new_report),
            ],
            "Azioni...": [
                ("Modifica path", self.controller.update_path),
                ("Smista screen Sanity", self.controller.sanity_paste),
                ("Device Manager", self.open_device_manager),
            ],
        }

        for label, commands in menu_structure.items():
            submenu = self.build_submenu(menu_bar, commands)
            menu_bar.add_cascade(label=label, menu=submenu)

        self.config(menu=menu_bar)

    def build_submenu(self, parent_menu, items):
        """
        Create a menu with commands and separators between entries.
        """
        submenu = tk.Menu(parent_menu, tearoff=0)
        for i, (label, command) in enumerate(items):
            submenu.add_command(label=label, command=command)
            if i < len(items) - 1:
                submenu.add_separator()
        return submenu

    def open_device_manager(self):
        """
        Launch the device manager window.
        """
        DeviceManagerWindow(self)

    def create_layout(self):
        """
        Place signature and note panels using consistent padding.
        """
        signature_panel = SignaturePanel(master=self)
        note_panel = NotePanel(master=self)
        watcher_panel = WatcherPanel(master=self)

        signature_panel.grid(row=0,column=1,padx=30,pady=15)
        note_panel.grid(row=1,column=1)
        watcher_panel.grid(row=0,column=2,padx=30)
