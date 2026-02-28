import json
import os
from PySide6.QtCore import QStandardPaths
from logger import logger

class SettingsManager:
    """Manages persistent application settings using a JSON file."""
    
    def __init__(self):
        self.settings_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        
        # Default settings
        self.settings = {
            "theme": "dark",
            "opacity": 95,
        }
        
        if not os.path.exists(self.settings_dir):
            os.makedirs(self.settings_dir, exist_ok=True)
            
        self.load_settings()

    def load_settings(self):
        """Load settings from the JSON file if it exists."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Update defaults with loaded values
                    self.settings.update(loaded)
                logger.info("Settings loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")

    def save_settings(self):
        """Save current settings to the JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
