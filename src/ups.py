import os
import json
import subprocess
import time

class UPSManager:
    def __init__(self, config_store, nut_user, nut_password):
        self.config_store = config_store
        self.nut_user = nut_user
        self.nut_password = nut_password

    def estimate_charge(self, voltage_str, status_str="OL", load_str="0"):
        try:
            v = float(voltage_str)
        except (ValueError, TypeError):
            return "NA"

        try:
            load = float(load_str) if load_str and load_str != "NA" else 0.0
        except (ValueError, TypeError):
            load = 0.0

        status = (status_str or "OL").upper()
        is_on_battery = "OB" in status or "DISCHRG" in status or "LB" in status
        is_24v = v > 18.0

        if is_24v:
            if is_on_battery:
                v_drop = (load / 100.0) * 1.2
                v_corrected = v + v_drop
                v_max = 25.2
                v_min = 21.0
                pct = ((v_corrected - v_min) / (v_max - v_min)) * 100.0
            else:
                if v >= 26.5:
                    pct = 100.0
                else:
                    pct = ((v - 24.0) / 2.5) * 100.0
        else:
            if is_on_battery:
                v_drop = (load / 100.0) * 0.6
                v_corrected = v + v_drop
                v_max = 12.6
                v_min = 10.5
                pct = ((v_corrected - v_min) / (v_max - v_min)) * 100.0
            else:
                if v >= 13.25:
                    pct = 100.0
                else:
                    pct = ((v - 12.0) / 1.25) * 100.0

        pct = min(max(pct, 0.0), 100.0)
        return f"{pct:.1f}"

    def get_status(self, ups_name):
        try:
            result = subprocess.run(['upsc', f'{ups_name}@localhost'], capture_output=True, text=True, timeout=3)
            if result.returncode != 0:
                return {"error": result.stderr.strip() or "Device not communicating"}
            data = {}
            for line in result.stdout.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    data[key.strip()] = val.strip()
            
            if 'battery.charge' not in data and 'battery.voltage' in data:
                est_charge = self.estimate_charge(
                    data['battery.voltage'],
                    data.get('ups.status', 'OL'),
                    data.get('ups.load', '0')
                )
                if est_charge != "NA":
                    data['battery.charge'] = est_charge
                    data['battery.charge.estimated'] = "true"
                    
            return data
        except Exception as e:
            return {"error": str(e)}

    def toggle_beeper(self, ups_name):
        result = subprocess.run([
            'upscmd', '-u', self.nut_user, '-p', self.nut_password,
            f'{ups_name}@localhost', 'beeper.toggle'
        ], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Failed to execute upscmd")
        return {"status": "success"}

    def control_load(self, ups_name, action):
        cmd_map = {
            'on': 'load.on',
            'off': 'load.off',
            'shutdown_return': 'shutdown.return',
            'shutdown_stayoff': 'shutdown.stayoff',
            'shutdown_stop': 'shutdown.stop'
        }
        if action not in cmd_map:
            raise ValueError("Invalid action")
        cmd = cmd_map[action]
        
        result = subprocess.run([
            'upscmd', '-u', self.nut_user, '-p', self.nut_password,
            f'{ups_name}@localhost', cmd
        ], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"Failed to execute upscmd {cmd}")
        return {"status": "success"}

    def set_variable(self, ups_name, var_name, var_val):
        if var_name not in ['ups.delay.shutdown', 'ups.delay.start']:
            raise ValueError("Unsupported or forbidden variable")
        
        try:
            val_int = int(var_val)
            if var_name == 'ups.delay.shutdown' and not (12 <= val_int <= 540):
                raise ValueError("Shutdown delay must be between 12 and 540 seconds")
            if var_name == 'ups.delay.start' and not (60 <= val_int <= 599940):
                raise ValueError("Start delay must be between 60 and 599940 seconds")
        except ValueError as ve:
            raise ValueError(f"Invalid value format: {str(ve)}")
        
        result = subprocess.run([
            'upsrw', '-s', f'{var_name}={var_val}',
            '-u', self.nut_user, '-p', self.nut_password,
            f'{ups_name}@localhost'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"Failed to set variable {var_name}")
        return {"status": "success"}


class AmbientSensorManager:
    def __init__(self, config_store, sensors_path='/opt/nut-dashboard/sensors.json'):
        self.config_store = config_store
        self.sensors_path = sensors_path

    def get_sensors_data(self):
        if os.path.exists(self.sensors_path):
            try:
                with open(self.sensors_path, 'r') as f:
                    sensors = json.load(f)
                    result = []
                    for mac, data in sensors.items():
                        data["stale"] = (time.time() - data.get("timestamp", 0) > 300)
                        short_mac = mac[-5:] if len(mac) >= 5 else mac
                        default_name = f"Sensor ({short_mac})"
                        data["display_name"] = self.config_store.get(f"sensor_{mac}_name", default_name)
                        result.append(data)
                    result.sort(key=lambda x: x["mac"])
                    return result
            except Exception:
                pass
        return []
