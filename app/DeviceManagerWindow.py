import tkinter as tk

from tkinter import ttk
from tkinter import messagebox

from .DevicePopup import DevicePopup
from controller import ControllerV3 as CT

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
                self.controller.device_command("delete", id=str(device_id))
                self.populate_tree()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
