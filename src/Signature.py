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
                self.combine.append(f"{_(key)} {entry}") #type: ignore - it's a builtin, check Localization.py
            except TypeError:
                messagebox.showerror(_("Error"), _("Invalid input - {field}").format(field=_(key))) #type: ignore - it's a builtin, check Localization.py

        self.combine.append(f"{_('DATA E ORA')} {time_responser('datetime')}") #type: ignore - it's a builtin, check Localization.py
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


def _signature_field_labels_for_extraction():  # pragma: no cover
    """
    Never called at runtime. The field labels above are translated
    dynamically (`_(field)`, where `field` is a variable), so static
    extraction tools like pybabel/xgettext can't discover them on their
    own. Listing them here as literal `_()` calls makes sure they end up
    in the .pot catalog. Keep this in sync with the field names used in
    Signature/SignatureSanity/SignatureMinimal.
    """
    return [
        _("Sigla"), _("BT"), _("APP"), _("BUILD"), _("DEVICE"), _("OS"), # type: ignore
        _("Puntamento"), _("CLONE"), _("BROWSER"), #type:ignore
    ]