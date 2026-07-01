import os
import sys

# Add current zip file or directory to path just in case
sys.path.insert(0, os.path.dirname(__file__))

from config import ConfigStore
from firmware import FirmwareManager
from ups import UPSManager, AmbientSensorManager
from history import HistoryLogger
from server import DashboardServer

PORT = 8080
VERSION = "0.4"

def main():
    # Dry-run validation check for zipapp self-update verification
    if os.environ.get('TEST_RUN') == '1':
        print(f"Dry-run verification of dashboard zipapp version {VERSION} passed.")
        sys.exit(0)

    # Initialize configuration store
    config_store = ConfigStore()

    # Load credentials
    nut_user = os.environ.get('NUT_USER', 'monuser')
    nut_password = os.environ.get('NUT_PASSWORD', 'secretpassword')

    # Initialize subsystems
    ups_manager = UPSManager(config_store, nut_user, nut_password)
    sensor_manager = AmbientSensorManager(config_store)
    history_logger = HistoryLogger(ups_manager)
    firmware_manager = FirmwareManager(current_version=VERSION)

    # Initialize and start HTTP server
    server = DashboardServer(
        port=PORT,
        config_store=config_store,
        ups_manager=ups_manager,
        sensor_manager=sensor_manager,
        history_logger=history_logger,
        firmware_manager=firmware_manager
    )
    server.serve()

if __name__ == '__main__':
    main()
