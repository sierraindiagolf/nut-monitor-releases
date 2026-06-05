import os
import glob
import sys

# Physical port platform addresses
# ups1 (2000VA) is connected to the USB controller at 5310400
# ups2 (1000VA) is connected to the USB controller at 5311400
PLATFORM_UPS_MAP = {
    "ups1": "5310400",  # 2000VA
    "ups2": "5311400"   # 1000VA
}

UPS_CONF_TEMPLATE = """maxretry = 3

[ups1]
    driver = nutdrv_qx
    port = auto
    vendorid = 0665
    productid = 5161
    bus = {ups1_bus}
    desc = "First UPS"
    default.battery.voltage.low = 21.0
    default.battery.voltage.high = 25.2
    default.battery.voltage.nominal = 24.0
    override.ups.power.nominal = 2000
    override.ups.realpower.nominal = 1200

[ups2]
    driver = nutdrv_qx
    port = auto
    vendorid = 0665
    productid = 5161
    bus = {ups2_bus}
    desc = "Second UPS"
    default.battery.voltage.low = 21.0
    default.battery.voltage.high = 25.2
    default.battery.voltage.nominal = 24.0
    override.ups.power.nominal = 1000
    override.ups.realpower.nominal = 600
"""

def get_bus_number(platform_addr):
    path = f"/sys/devices/platform/soc/{platform_addr}.usb/usb*"
    dirs = glob.glob(path)
    if dirs:
        dirname = os.path.basename(dirs[0])
        bus_str = dirname.replace("usb", "")
        try:
            return f"{int(bus_str):03d}"
        except ValueError:
            pass
    return None

def main():
    ups1_bus = get_bus_number(PLATFORM_UPS_MAP["ups1"])
    ups2_bus = get_bus_number(PLATFORM_UPS_MAP["ups2"])
    
    if not ups1_bus or not ups2_bus:
        print(f"Error: Could not resolve bus numbers. ups1: {ups1_bus}, ups2: {ups2_bus}")
        sys.exit(1)
        
    print(f"Resolved buses - ups1 (2000VA): {ups1_bus}, ups2 (1000VA): {ups2_bus}")
    
    new_conf = UPS_CONF_TEMPLATE.format(ups1_bus=ups1_bus, ups2_bus=ups2_bus)
    
    conf_path = "/etc/nut/ups.conf"
    
    current_conf = ""
    if os.path.exists(conf_path):
        with open(conf_path, "r") as f:
            current_conf = f.read()
            
    if current_conf.strip() != new_conf.strip():
        print("Configuration changed. Writing new /etc/nut/ups.conf...")
        with open(conf_path, "w") as f:
            f.write(new_conf)
        os.chmod(conf_path, 0o640)
        try:
            import pwd
            import grp
            uid = pwd.getpwnam("root").pw_uid
            gid = grp.getgrnam("nut").gr_gid
            os.chown(conf_path, uid, gid)
        except Exception as e:
            print(f"Warning: Could not set owner/group on {conf_path}: {e}")
            
        print("Configuration updated successfully.")
    else:
        print("Configuration is already up to date.")

if __name__ == "__main__":
    main()
