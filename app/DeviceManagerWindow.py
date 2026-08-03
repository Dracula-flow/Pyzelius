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
        self.title(_("Device Manager")) # type: ignore
        self.geometry("625x300")
        self.controller = CT(self)

        self.columns = ("ID", "Device", "OS")
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=_(col)) # type: ignore
        self.tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Buttons
        btn_cfg = [
            (_("Add Device"), self.open_add_popup), # type: ignore
            (_("Modify Device"), self.open_modify_popup), # type: ignore
            (_("Delete Device"), self.delete_selected_device) # type: ignore
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
            messagebox.showwarning(_("Selection Error"), _("Please select a device to modify.")) # type: ignore
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
            messagebox.showwarning(_("Selection Error"), _("Please select a device to delete.")) # type: ignore
            return

        # NOTE: the third value is intentionally unused, but must NOT be named
        # "_" here, since that would shadow the gettext translation function.
        device_id, device_name, _unused_os = self.tree.item(selected_item, "values")
        confirm = messagebox.askyesno(
            _("Confirm Delete"), # type: ignore
            _("Delete device '{name}' (ID: {id})?").format(name=device_name, id=device_id) # type: ignore
        )
        if confirm:
            try:
                self.controller.device_command("delete", id=int(device_id))
                self.populate_tree()
            except ValueError as e:
                messagebox.showerror(_("Error"), str(e)) # type: ignore


def _device_manager_column_labels_for_extraction():  # pragma: no cover
    """
    Never called at runtime - see the matching note in src/Signature.py.
    Column names are translated dynamically (`_(col)`), so list the
    literals here for pybabel/xgettext to pick up.
    """
    return [_("ID"), _("Device"), _("OS")] # type: ignore
