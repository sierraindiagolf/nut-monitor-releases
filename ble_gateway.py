import asyncio
import json
import os
import time
from bleak import BleakScanner

SENSORS_JSON_PATH = '/opt/nut-dashboard/sensors.json'
TARGET_UUID = "ebefd08370a247c89837e7b5634df525"

# Load existing sensor states on startup to prevent transient loss
active_sensors = {}
try:
    if os.path.exists(SENSORS_JSON_PATH):
        with open(SENSORS_JSON_PATH, 'r') as f:
            active_sensors = json.load(f)
except Exception as e:
    print(f"Error loading initial sensors: {e}")

def parse_jaalee_ibeacon(data):
    if len(data) < 24:
        return None
    # check prefix
    if data[0] != 0x02 or data[1] != 0x15:
        return None
    # check UUID
    uuid_bytes = data[2:18]
    uuid_hex = uuid_bytes.hex()
    if uuid_hex != TARGET_UUID:
        return None
    
    # Major (Temperature)
    temp_raw = (data[18] << 8) | data[19]
    # Minor (Humidity)
    humi_raw = (data[20] << 8) | data[21]
    # Battery
    battery = data[23]
    
    temp = (temp_raw / 65535.0) * 175.0 - 45.0
    humi = (humi_raw / 65535.0) * 100.0
    
    return {
        "temperature": round(temp, 1),
        "humidity": round(humi, 1),
        "battery": battery
    }

def detection_callback(device, advertisement_data):
    # Manufacturer data is a dict: {company_id: bytes}
    # Apple company ID is 76 (0x004c)
    mfr_data = advertisement_data.manufacturer_data
    if 76 in mfr_data:
        parsed = parse_jaalee_ibeacon(mfr_data[76])
        if parsed:
            mac = device.address
            parsed["timestamp"] = int(time.time())
            parsed["mac"] = mac
            active_sensors[mac] = parsed
            
            # Write to a temporary file first, then rename to ensure atomicity
            temp_path = SENSORS_JSON_PATH + ".tmp"
            try:
                with open(temp_path, 'w') as f:
                    json.dump(active_sensors, f)
                os.chmod(temp_path, 0o644)
                os.replace(temp_path, SENSORS_JSON_PATH)
            except Exception as e:
                print(f"Error saving sensors data: {e}")

async def main():
    print("Starting NUT BLE Sensor Gateway...")
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    while True:
        await asyncio.sleep(3600)  # Keep running indefinitely

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping gateway...")
