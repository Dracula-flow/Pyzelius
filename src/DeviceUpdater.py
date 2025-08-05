import json

from pathlib import Path

class DeviceUpdater:
    """
    Handles the updating of the Devices memorized in the JSON file. It behaves with a database-like logic.
    Each device will an ID, assigned automatically.
    """
    def __init__(self, json_path: Path):
        self.json_path = json_path
        self.config_data = self.device_getter()

    def device_getter(self):
        with open(self.json_path, "r") as f:
            return json.load(f)
        
    def ensure_device_key(self):
        if "Devices" not in self.config_data:
            self.config_data["Devices"] = {}  
    
    def JSON_writer(self):
        with open(self.json_path, "w") as w:
            json.dump(self.config_data, w, indent=4)

    def add_entry(self, new_device: str, new_os: str):
        "Adds a device entry to the JSON file"
        # Ensure that the "Devices" key exists in the JSON structure
        self.ensure_device_key()

        # Generate a new ID based on the existing ones
        new_id = int(len(self.config_data["Devices"]) + 1)

        # Add the new device entry with the generated ID
        self.config_data["Devices"][new_id] = {
            "device": new_device,
            "os": new_os
        }

        # Write the updated JSON data back to the file
        self.JSON_writer()

    def modify_entry(self, device_id: int, new_device: str, new_os: str):
        "Modifies a device entry by ID, provided there are new arguments"
        self.ensure_device_key()

             # Check if the device ID exists
        if device_id in self.config_data["Devices"]:
            # Modify the device entry
            self.config_data["Devices"][device_id]["device"] = new_device
            self.config_data["Devices"][device_id]["os"] = new_os
            self.JSON_writer()  # Save changes to the file
        else:
            raise ValueError(f"Device ID '{device_id}' does not exist in the configuration.")

        self.JSON_writer()

    def delete_entry(self, device_id:str):
        """Deletes a device entry by ID."""
        self.ensure_device_key()

        # Check if the device ID exists
        if device_id in self.config_data["Devices"]:
            # Remove the device entry
            del self.config_data["Devices"][device_id]
            self.JSON_writer()  # Save changes to the file
        else:
            raise ValueError(f"Device ID '{device_id}' does not exist in the configuration.")
    
    def load_devices(self, tree: object):
        try:
            with open(self.json_path, "r") as file:
                data = json.load(file)
                devices = data.get("Devices", {})
                for device_id, device_info in devices.items():
                    tree.insert("", "end", values=(device_id, device_info["device"], device_info["os"]))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading devices: {e}")
