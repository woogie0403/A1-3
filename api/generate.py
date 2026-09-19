from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        response_data = {"status": "ok", "message": "TripSketch API is ready"}
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
