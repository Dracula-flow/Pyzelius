from typing import List

import pyperclip
from src import Signature, SignatureSanity, SignatureMinimal

class SignatureController:
    """
    Handles the logic pertaining to the Signature class and signature generation.
    """
    def __init__(self, mode: str= "Full"):
        self.signature = self.get_signature_class(mode)

    def get_signature_class(self, mode:str) -> Signature:
        classes = {
            "Full" : Signature,
            "Sanity": SignatureSanity,
            "Simple":SignatureMinimal
            }
        return classes.get(mode,Signature)() #Defaults to signature if mode, for some reason, is unknown
    
    def generate_signature(self, entry_values: List[str])-> str:
        """
        Combines the various inputs in the entry fields and generates a formatted signature string.
        """
        return self.signature.entry_combine(entry_values)
    
    def copy_to_clipboard(self, entry_values: List[str])-> None:
        """
        Generates the signature and copies it to the clipboard.
        """
        result = self.generate_signature(entry_values)
        pyperclip.copy(result)

    def get_fields(self) -> List[str]:
        """
        Returns the input field labels for the selected signature.
        Helps build the correct number of fields in the GUI.
        """
        return list(self.signature.input_fields)