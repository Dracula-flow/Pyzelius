from tkinter import messagebox

from .Functions import time_responser

class Signature():
    """
    Generates a signature necessary to close a test. It has to be mounted on a Tkinter frame.
    """
    def __init__(self):
        self.input_fields = ("Sigla", 
                "BT",
                "APP",
                "BUILD", 
                "DEVICE",
                "OS",
                "Puntamento")
        self.combine=[]

    def entry_combine(self, entry_list):
        self.combine.clear()
        for entry,key in zip(entry_list,self.input_fields):
            try:
                # input_value= entry.get()
                self.combine.append(f"{key} {entry}")
            except TypeError:
                messagebox.showerror (f"Error: Invalid Input - {key}")

        self.combine.append(f"{'DATA E ORA'} {time_responser('datetime')}")
        self.result = "\n".join(self.combine)
        return self.result
    
class SignatureSanity(Signature):
    """
    Signature subclass with fewer fields.
    """
    def __init__(self):
        super().__init__()
        self.input_fields = ("Sigla", "BT", "CLONE", "BROWSER",)  # Subclass with fewer fields

class SignatureMinimal(Signature):
    """
    Signature class with just the initials.
    """
    def __init__(self):
        super().__init__()
        self.input_fields = ("Sigla",) # The comma is necessary, otherwise the entry_combine will interpret this as a string to split