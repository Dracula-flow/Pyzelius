# Author: Simone Avagliano
# Date Created: 25/02/2025
# Description: Pyzelius v.1.8.0, a dashboard to help manual testing
# License: Creative Commons Zero v1.0 Universal

# Simple launcher for the app

from src import Pathfinder as PF
from src.Localization import Localization

if __name__ == "__main__":
    # Load the saved (or default) language and install `_()` globally
    # before anything else is imported/built, so every module below can
    # use it right away.
    Localization.install(config_path=PF().get_config_path())

    from app.GuiV3 import Gui

    app = Gui()
    app.mainloop()