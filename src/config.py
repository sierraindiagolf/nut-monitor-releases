import json
import os

class ConfigStore:
    def __init__(self, config_path='/opt/nut-dashboard/config.json'):
        self.config_path = config_path
        self.config = self._load()

    def _load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "ups1_name": "UPS Unit 1",
            "ups2_name": "UPS Unit 2"
        }

    def save(self, config_data):
        for k, v in config_data.items():
            if k in ["ups1_name", "ups2_name"] or k.startswith("sensor_"):
                self.config[k] = v.strip()
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception:
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)
