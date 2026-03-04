import tkinter as tk

from tkinter import messagebox

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
                self.controller.device_command("add", device=device_name, os=os_version)
            elif self.action == "modify":
                self.controller.device_command("modify", id=self.device_id, device=device_name, os=os_version)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            if self.on_close:
                self.on_close()
            self.destroy() 