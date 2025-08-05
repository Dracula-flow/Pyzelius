from pathlib import Path
from typing import Optional

from src import Archiver

from watchdog.observers import Observer

class WatcherController:
    """
    Handles the business logic regarding the Archiver class, specifically:
    - The gathering of string types in the dedicated Entry field.
    - The initialization and termination of the process.

    """
    def __init__(self, path: Path):
        self.path = path
        self.observer: Optional[Observer] = None # type: ignore

    def start_watching(self, entry:object):
        template = entry.get().strip()
        event_handler = Archiver(template)

        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=False)
        self.observer.start()

    def stop_watching(self):
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
        else:
            print("Error.")