import tkinter as tk
from tkinter import ttk

from controller import ControllerV3 as CT

from src import apply_char_limit

class SignatureTab(ttk.Frame):
    """
    A single tab within the SignaturePanel.
    """
    def __init__(self, parent, mode:str, config_data, controller):
        super().__init__(parent)
        self.mode = mode
        self.controller = controller
        self.config_data = config_data
        self.entry_list = []
        self.os_entry = None
        self.input_fields = self.controller.get_signature_fields(mode)
        
        self.build_fields()
        self.build_button()

    def build_fields(self):
        for i, field in enumerate(self.input_fields):
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
        btn.grid(row=len(self.input_fields), column=0, columnspan=2, pady=20)

    def on_copy(self):
        values = [e.get() for e in self.entry_list]
        if self.os_entry:
            values.insert(self.input_fields.index("OS"), self.os_entry.get())
        self.controller.on_copy_signature(values,self.mode)


class SignaturePanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = CT(self)
        self.config_data = self.controller.device_controller.get_devices()
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        signature_types = ["Full","Sanity","Simple"]

        for mode in signature_types:
            tab = SignatureTab(tab_control, mode, self.config_data, self.controller)
            tab_control.add(tab, text=mode)
            tab.bind("<Alt-d>", lambda e: tab.on_copy())

        tab_control.pack(expand=1, fill="none")


