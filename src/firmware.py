import json
import os
import sys
import subprocess
import urllib.request

class FirmwareManager:
    def __init__(self, current_version="0.4", repo="sierraindiagolf/nut-monitor-releases"):
        self.current_version = current_version
        self.repo = repo

    def fetch_tags(self):
        url = f"https://api.github.com/repos/{self.repo}/tags"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python-urllib/3.x'}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                tags = [tag.get('name') for tag in data if 'name' in tag]
                return tags
        except Exception as e:
            sys.stderr.write(f"Error fetching github tags: {e}\n")
            return []

    def download_file(self, tag):
        url = f"https://raw.githubusercontent.com/{self.repo}/{tag}/dashboard.pyz"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python-urllib/3.x'}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read()
        except Exception as e:
            sys.stderr.write(f"Error downloading dashboard.pyz at {tag}: {e}\n")
            return None

    def check_updates(self):
        tags = self.fetch_tags()
        latest_version = self.current_version
        update_available = False
        versions_list = []
        
        for tag in tags:
            v_clean = tag.lstrip('v')
            versions_list.append(tag)
            try:
                curr_parts = [int(p) for p in self.current_version.split('.')]
                tag_parts = [int(p) for p in v_clean.split('.')]
                if tag_parts > curr_parts:
                    latest_clean = latest_version.lstrip('v')
                    latest_parts = [int(p) for p in latest_clean.split('.')]
                    if tag_parts > latest_parts:
                        latest_version = tag
                        update_available = True
            except Exception:
                pass
        
        return {
            "current_version": f"v{self.current_version}",
            "latest_version": latest_version if latest_version.startswith('v') else f"v{latest_version}",
            "update_available": update_available,
            "versions": versions_list
        }

    def update_firmware(self, version):
        code_bytes = self.download_file(version)
        if not code_bytes:
            raise RuntimeError(f"Could not download dashboard.pyz for version {version}")
        
        current_file_path = os.path.abspath(sys.argv[0])
        temp_path = current_file_path + '.tmp'
        
        with open(temp_path, 'wb') as f:
            f.write(code_bytes)
        
        # Dry-run validation
        res = subprocess.run(['python3', temp_path], env={**os.environ, 'TEST_RUN': '1'}, capture_output=True)
        if res.returncode != 0:
            err_msg = res.stderr.decode('utf-8').strip()
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise RuntimeError(f"Package validation failed:\n{err_msg}")
        
        os.replace(temp_path, current_file_path)
        
        import threading
        def restart_soon():
            import time
            time.sleep(1.0)
            os._exit(0)
        threading.Thread(target=restart_soon).start()
