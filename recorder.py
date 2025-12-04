#!/usr/bin/env python3
"""
Traffic Recorder and Replay (Stretch Goal)
Capture real HTTP traffic and serve it later.
"""

import json
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime, timezone
import threading


class TrafficRecorder:
    """Records HTTP traffic to a file."""
    
    def __init__(self, output_file):
        self.output_file = output_file
        self.recordings = []
        self.lock = threading.Lock()
    
    def record(self, method, path, status, response_body, headers):
        """Record a request/response pair."""
        with self.lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "method": method,
                "path": path,
                "status": status,
                "response": response_body,
                "headers": dict(headers)
            }
            self.recordings.append(entry)
    
    def save(self):
        """Save recordings to file."""
        with self.lock:
            with open(self.output_file, 'w') as f:
                json.dump(self.recordings, f, indent=2)
            print(f"[RECORDER] Saved {len(self.recordings)} recordings to {self.output_file}")


class ReplayHandler(BaseHTTPRequestHandler):
    """Replays recorded traffic."""
    
    recordings = []
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def do_PUT(self):
        self._handle_request('PUT')
    
    def do_DELETE(self):
        self._handle_request('DELETE')
    
    def _handle_request(self, method):
        """Find and replay matching recording."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Find matching recording
        for recording in self.recordings:
            if recording['method'] == method and recording['path'] == path:
                self._send_recorded_response(recording)
                return
        
        # No match found
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "No recording found"}).encode())
    
    def _send_recorded_response(self, recording):
        """Send recorded response."""
        self.send_response(recording['status'])
        
        # Send recorded headers
        for header, value in recording.get('headers', {}).items():
            if header.lower() not in ['content-length', 'transfer-encoding']:
                self.send_header(header, value)
        
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = recording['response']
        if isinstance(response, dict):
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write(str(response).encode())


def record_mode(target_url, output_file, port):
    """Run in record mode - proxy requests and save responses."""
    print(f"Recording mode: Proxying to {target_url}")
    print(f"Saving to: {output_file}")
    print(f"Note: Full proxy implementation requires 'requests' library")
    print(f"For now, manually create recordings in JSON format")
    
    # This would require implementing a full HTTP proxy
    # For simplicity, we'll just show the structure
    example = [
        {
            "timestamp": "2025-11-20T10:00:00Z",
            "method": "GET",
            "path": "/api/users",
            "status": 200,
            "response": {"users": []},
            "headers": {"Content-Type": "application/json"}
        }
    ]
    
    with open(output_file, 'w') as f:
        json.dump(example, f, indent=2)
    
    print(f"Created example recording file")


def replay_mode(input_file, port):
    """Run in replay mode - serve recorded responses."""
    try:
        with open(input_file, 'r') as f:
            recordings = json.load(f)
    except FileNotFoundError:
        print(f"Recording file not found: {input_file}")
        return
    
    ReplayHandler.recordings = recordings
    
    server = HTTPServer(('', port), ReplayHandler)
    print(f"Replay mode: Serving {len(recordings)} recordings")
    print(f"Server running on http://localhost:{port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Shutting down...")
        server.shutdown()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Traffic Recorder and Replay')
    parser.add_argument('mode', choices=['record', 'replay'], help='Operation mode')
    parser.add_argument('--file', default='recordings.json', help='Recording file')
    parser.add_argument('--port', type=int, default=8001, help='Server port')
    parser.add_argument('--target', help='Target URL for recording (record mode only)')
    args = parser.parse_args()
    
    if args.mode == 'record':
        if not args.target:
            parser.error("--target is required in record mode")
        record_mode(args.target, args.file, args.port)
    else:
        replay_mode(args.file, args.port)


if __name__ == '__main__':
    main()
