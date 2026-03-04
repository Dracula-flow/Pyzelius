from pathlib import Path
from typing import Dict,Optional

from src import DeviceUpdater

class DeviceController:
    """
    Handles the business logic between the DeviceUpdater backend class and the DeviceManager frontend class.
    """
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.devices = DeviceUpdater(config_path)

    def load_devices(self, tree: object) -> None:
        """Load devices into given tree tkinter widget."""
        self.devices.load_devices(tree)

    def get_devices(self) -> Dict[str, dict]:
        """Return devices dictionary from config.json"""
        import json
        with open(self.config_path, "r") as f:
            config_data = json.load(f)
        return config_data.get("Devices", {})

    def on_device_select(self, device_name: str) -> Optional[str]:
        """Return OS of selected device name or None if not found."""
        config_data = self.get_devices()
        for device_id, data in config_data.items():
            if data.get("device") == device_name:
                return data.get("os", None)
        return None

    def device_manager_commands(self, selector: str, id: str = "", device: str = "", os: str = "") -> None:
        """Add, modify, or delete device entry."""
        actions = {
            'add': lambda: self.devices.add_entry(device, os),
            'modify': lambda: self.devices.modify_entry(id, device, os),
            'delete': lambda: self.devices.delete_entry(id),
        }
        if selector not in actions:
            raise ValueError(f"Invalid selector '{selector}'. Use 'add', 'modify', or 'delete'.")
        actions[selector]()