# Define the __all__ variable for eventuale of wildcard (*) imports
__all__ = ["Gui",
            "DeviceManagerWindow",
            "DevicePopup",
            "NotePanel",
            "SignaturePanel",
            "WatcherPanel"
           ]

# Define the single modules
from .GuiV3 import Gui
from .DeviceManagerWindow import DeviceManagerWindow
from .DevicePopup import DevicePopup
from .NotePanel import NotePanel
from .SignaturePanel import SignaturePanel
from .WatcherPanel import WatcherPanel