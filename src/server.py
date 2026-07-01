import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from ui import HTML_CONTENT

class DashboardHandler(BaseHTTPRequestHandler):
    config_store = None
    ups_manager = None
    sensor_manager = None
    history_logger = None
    firmware_manager = None

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        elif url.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            status = {
                "ups1": {**self.ups_manager.get_status("ups1"), "display_name": self.config_store.get("ups1_name", "UPS Unit 1")},
                "ups2": {**self.ups_manager.get_status("ups2"), "display_name": self.config_store.get("ups2_name", "UPS Unit 2")},
                "ambient_sensors": self.sensor_manager.get_sensors_data()
            }
            self.wfile.write(json.dumps(status).encode('utf-8'))
        elif url.path == '/api/history':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            query_params = urllib.parse.parse_qs(url.query)
            start_str = query_params.get('start', [None])[0]
            end_str = query_params.get('end', [None])[0]
            history = {
                "ups1": self.history_logger.get_history("ups1", start_str, end_str),
                "ups2": self.history_logger.get_history("ups2", start_str, end_str)
            }
            self.wfile.write(json.dumps(history).encode('utf-8'))
        elif url.path == '/api/battery-health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            health_data = {
                "ups1": self.history_logger.analyze_outages("ups1"),
                "ups2": self.history_logger.analyze_outages("ups2")
            }
            self.wfile.write(json.dumps(health_data).encode('utf-8'))
        elif url.path == '/api/firmware/check':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = self.firmware_manager.check_updates()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == '/api/config':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                config_data = json.loads(post_data.decode('utf-8'))
                
                success = self.config_store.save(config_data)
                if not success:
                    raise RuntimeError("Failed to write config file")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif url.path == '/api/beeper/toggle':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                req_data = json.loads(post_data.decode('utf-8'))
                ups_name = req_data.get('ups')
                if ups_name not in ['ups1', 'ups2']:
                    raise ValueError("Invalid UPS name")
                
                response = self.ups_manager.toggle_beeper(ups_name)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif url.path == '/api/load/control':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                req_data = json.loads(post_data.decode('utf-8'))
                ups_name = req_data.get('ups')
                action = req_data.get('action')
                if ups_name not in ['ups1', 'ups2']:
                    raise ValueError("Invalid UPS name")
                
                response = self.ups_manager.control_load(ups_name, action)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif url.path == '/api/config/variable':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                req_data = json.loads(post_data.decode('utf-8'))
                ups_name = req_data.get('ups')
                var_name = req_data.get('var')
                var_val = req_data.get('value')
                
                if ups_name not in ['ups1', 'ups2']:
                    raise ValueError("Invalid UPS name")
                
                response = self.ups_manager.set_variable(ups_name, var_name, var_val)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif url.path == '/api/firmware/update':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                req_data = json.loads(post_data.decode('utf-8'))
                version = req_data.get('version')
                if not version:
                    raise ValueError("Version is required")
                
                self.firmware_manager.update_firmware(version)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": f"Successfully updated to {version}. Restarting server..."}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


class DashboardServer:
    def __init__(self, port, config_store, ups_manager, sensor_manager, history_logger, firmware_manager):
        self.port = port
        DashboardHandler.config_store = config_store
        DashboardHandler.ups_manager = ups_manager
        DashboardHandler.sensor_manager = sensor_manager
        DashboardHandler.history_logger = history_logger
        DashboardHandler.firmware_manager = firmware_manager
        self.server = HTTPServer(('127.0.0.1', self.port), DashboardHandler)

    def serve(self):
        print(f"Starting server on port {self.port}...")
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        print("Server stopped.")
