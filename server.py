#!/usr/bin/env python3
import http.server
import json
import os
import socket
import threading
from datetime import datetime

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'participants.json')
lock = threading.Lock()


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/register':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                participant = json.loads(body)
                with lock:
                    data = load()
                    data.append(participant)
                    save(data)
                self._json(200, {'ok': True})
            except Exception as e:
                self._json(400, {'error': str(e)})
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith('/api/participants/'):
            pid = self.path.split('/')[-1]
            with lock:
                data = [p for p in load() if p.get('id') != pid]
                save(data)
            self._json(200, {'ok': True})
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith('/api/participants/'):
            pid = self.path.split('/')[-1]
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                updates = json.loads(body)
                with lock:
                    data = load()
                    for i, p in enumerate(data):
                        if p.get('id') == pid:
                            data[i] = {**p, **updates}
                            break
                    save(data)
                self._json(200, {'ok': True})
            except Exception as e:
                self._json(400, {'error': str(e)})
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == '/api/participants':
            with lock:
                data = load()
            self._json(200, data)
        else:
            super().do_GET()

    def _json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[{datetime.now().strftime("%H:%M:%S")}] {fmt % args}')


if __name__ == '__main__':
    os.chdir(BASE_DIR)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = '127.0.0.1'

    with http.server.ThreadingHTTPServer(('', PORT), Handler) as httpd:
        print('=' * 50)
        print('  EMD Registration Server')
        print('=' * 50)
        print(f'  Local:     http://localhost:{PORT}/')
        print(f'  Network:   http://{local_ip}:{PORT}/')
        print()
        print(f'  Form:      http://{local_ip}:{PORT}/Registration%20Form.html')
        print(f'  Dashboard: http://{local_ip}:{PORT}/Event%20Dashboard.html')
        print()
        print('  Ctrl+C to stop')
        print('=' * 50)
        httpd.serve_forever()
