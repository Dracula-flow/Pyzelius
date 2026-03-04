import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from .Functions import time_responser

class Archiver(FileSystemEventHandler):
    """
    Automatically renames video files with a template inserted by the user. Works in conjunction with the Watcher class (GUI).
    """
    def __init__(self, template:str):
        super().__init__()
        self.template=template
        self.VIDEO_EXTENSIONS = ('.mp4','.mov')

    def on_created(self, event):
        # Delay to ensure file is fully copied
        time.sleep(1)

        if event.is_directory:
            return 
        
        file_path = Path(event.src_path)

        if file_path.suffix.lower() in self.VIDEO_EXTENSIONS:
            folder = file_path.parent
            timestamp = time_responser("time")
            safe_timestamp = timestamp.replace(":",".")

            template_str = self.template.strip() if self.template.strip() else "Video"
            
            new_name = f"{template_str} - {safe_timestamp}{file_path.suffix}"
            new_path = folder / new_name

            try:

                file_path.rename(new_path)
                print(f"Renamed: {file_path} -> {new_path}")
                
            except Exception as e:
                print(f"Error renaming file {file_path}: {e}")