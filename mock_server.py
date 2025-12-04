#!/usr/bin/env python3
"""
Local API Mock Server
Configurable HTTP server for testing with latency and failure simulation.
"""

import json
import time
import argparse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import random
import uuid
import re
import os
import mimetypes




class WishlistManager:
    """Manages in-memory wishlist storage."""
    
    def __init__(self):
        self.wishlist = []
        self.lock = threading.Lock()
    
    def get_all(self):
        """Get all wishlist items."""
        with self.lock:
            return list(self.wishlist)
    
    def add(self, title):
        """Add a game to wishlist."""
        with self.lock:
            # Check if already in wishlist
            if any(item['title'] == title for item in self.wishlist):
                return False, "Game already in wishlist"
            
            # Add new item
            item = {
                "title": title,
                "added_at": datetime.now(timezone.utc).isoformat(),
                "price": f"${random.randint(20, 80)}"
            }
            self.wishlist.append(item)
            return True, "Added to wishlist"
    
    def remove(self, title):
        """Remove a game from wishlist."""
        with self.lock:
            # Find and remove the item
            for i, item in enumerate(self.wishlist):
                if item['title'] == title:
                    self.wishlist.pop(i)
                    return True, "Removed from wishlist"
            return False, "Game not found in wishlist"
    
    def count(self):
        """Get total items in wishlist."""
        with self.lock:
            return len(self.wishlist)


class MockServerConfig:
    """Manages server configuration with hot-reload support."""
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}
        self.database = []
        self.lock = threading.Lock()
        self.load()
    
    def load(self):
        """Load configuration from JSON file."""
        with self.lock:
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                print(f"[CONFIG] Loaded from {self.config_path}")
                
                # Load database if specified
                db_path = self.config.get('database')
                if db_path:
                    self._load_database(db_path)
            except FileNotFoundError:
                print(f"[CONFIG] File not found: {self.config_path}")
                self.config = self._default_config()
            except json.JSONDecodeError as e:
                print(f"[CONFIG] Invalid JSON: {e}")
                self.config = self._default_config()
    
    def _load_database(self, db_path):
        """Load database from JSON file."""
        try:
            with open(db_path, 'r') as f:
                self.database = json.load(f)
            print(f"[DATABASE] Loaded {len(self.database)} records from {db_path}")
        except FileNotFoundError:
            print(f"[DATABASE] File not found: {db_path}")
            self.database = []
        except json.JSONDecodeError as e:
            print(f"[DATABASE] Invalid JSON: {e}")
            self.database = []
    
    def _default_config(self):
        """Return default configuration."""
        return {
            "port": 8000,
            "cors": True,
            "endpoints": []
        }
    
    def get(self, key, default=None):
        """Thread-safe config access."""
        with self.lock:
            return self.config.get(key, default)
    
    def find_endpoint(self, path, method):
        """Find matching endpoint configuration."""
        with self.lock:
            for endpoint in self.config.get('endpoints', []):
                if endpoint.get('path') == path and endpoint.get('method') == method:
                    return endpoint
        return None
    
    def get_database(self):
        """Get database records."""
        with self.lock:
            return list(self.database)
    
    def filter_database(self, field, value):
        """Filter database by field value."""
        with self.lock:
            return [record for record in self.database if record.get(field) == value]
    
    def find_in_database(self, field, value):
        """Find a single record in database by field value."""
        with self.lock:
            for record in self.database:
                if record.get(field) == value:
                    return record
        return None
    
    def filter_by_genre(self, genre):
        """Filter database by genre (checks if genre is in genres array)."""
        with self.lock:
            return [record for record in self.database 
                    if genre in record.get('genres', [])]
    

    def add_game(self, game_data):
        """Add a new game to the database."""
        with self.lock:
            # Check if game already exists
            title = game_data.get('title')
            if title and any(record.get('title') == title for record in self.database):
                return False, "Game already exists"
            
            self.database.append(game_data)
            return True, game_data
    
    def delete_game(self, identifier_field, identifier_value):
        """Delete a game from the database."""
        with self.lock:
            for i, record in enumerate(self.database):
                if record.get(identifier_field) == identifier_value:
                    deleted_game = self.database.pop(i)
                    return True, deleted_game
            return False, None


class RequestLogger:
    """Thread-safe request logger."""
    
    def __init__(self, max_logs=100):
        self.logs = []
        self.max_logs = max_logs
        self.lock = threading.Lock()
    
    def log(self, method, path, status, latency_ms):
        """Add a log entry."""
        with self.lock:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "method": method,
                "path": path,
                "status": status,
                "latency_ms": latency_ms
            }
            self.logs.append(entry)
            if len(self.logs) > self.max_logs:
                self.logs.pop(0)
    
    def get_logs(self):
        """Get all logs."""
        with self.lock:
            return list(self.logs)


class TemplateEngine:
    """Simple template engine for dynamic response fields."""
    
    @staticmethod
    def render(data, query_params, config):
        """Recursively render templates in data structure."""
        if isinstance(data, dict):
            return {k: TemplateEngine.render(v, query_params, config) for k, v in data.items()}
        elif isinstance(data, list):
            return [TemplateEngine.render(item, query_params, config) for item in data]
        elif isinstance(data, str):
            return TemplateEngine._render_string(data, query_params, config)
        return data
    
    @staticmethod
    def _render_string(template, query_params, config):
        """Render template string with variables."""
        # {{database}} - return entire database
        if template == '{{database}}':
            return config.get_database()
        
        # {{database_count}} - return database count
        if template == '{{database_count}}':
            return len(config.get_database())
        
        # {{database_filter:field:value}} - filter database (with query param support)
        filter_match = re.match(r'\{\{database_filter:(\w+):(.+)\}\}', template)
        if filter_match:
            field, value = filter_match.groups()
            # Check if value is a query param placeholder
            query_match = re.match(r'\{\{query\.(\w+)\}\}', value)
            if query_match:
                param_name = query_match.group(1)
                value = query_params.get(param_name, [''])[0]
            # Convert value to appropriate type
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
            return config.filter_database(field, value)
        
        # {{database_find:field:value}} - find single record (with query param support)
        find_match = re.match(r'\{\{database_find:(\w+):(.+)\}\}', template)
        if find_match:
            field, value = find_match.groups()
            # Check if value is a query param placeholder
            query_match = re.match(r'\{\{query\.(\w+)\}\}', value)
            if query_match:
                param_name = query_match.group(1)
                value = query_params.get(param_name, [''])[0]
            return config.find_in_database(field, value)
        
        # {{database_filter_genre:genre}} - filter by genre (with query param support)
        genre_match = re.match(r'\{\{database_filter_genre:(.+)\}\}', template)
        if genre_match:
            genre = genre_match.group(1)
            # Check if genre is a query param placeholder
            query_match = re.match(r'\{\{query\.(\w+)\}\}', genre)
            if query_match:
                param_name = query_match.group(1)
                genre = query_params.get(param_name, [''])[0]
            return config.filter_by_genre(genre)
        
        # {{query.param_name}} - replace with query parameter value (JSON-escaped)
        def replace_query(match):
            param_name = match.group(1)
            value = query_params.get(param_name, [''])[0]
            # Escape for JSON: quotes, backslashes, newlines, etc.
            value = value.replace('\\', '\\\\')  # Backslash first!
            value = value.replace('"', '\\"')    # Quotes
            value = value.replace('\n', '\\n')   # Newlines
            value = value.replace('\r', '\\r')   # Carriage returns
            value = value.replace('\t', '\\t')   # Tabs
            return value
        
        template = re.sub(r'\{\{query\.(\w+)\}\}', replace_query, template)
        
        # {{timestamp}}
        template = re.sub(
            r'\{\{timestamp\}\}',
            datetime.now(timezone.utc).isoformat(),
            template
        )
        
        # {{random_int}}
        template = re.sub(
            r'\{\{random_int\}\}',
            str(random.randint(0, 1000000)),
            template
        )
        
        # {{random_price}} - random price between $20-$80
        template = re.sub(
            r'\{\{random_price\}\}',
            f'${random.randint(20, 80)}',
            template
        )
        
        # {{uuid}}
        template = re.sub(
            r'\{\{uuid\}\}',
            str(uuid.uuid4()),
            template
        )
        
        return template


class MockRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with mock capabilities."""
    
    config = None
    logger = None
    wishlist_manager = None
    
    def do_GET(self):
        """Handle GET requests."""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests."""
        self._handle_request('POST')
    
    def do_DELETE(self):
        """Handle DELETE requests."""
        self._handle_request('DELETE')
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def _handle_request(self, method):
        """Main request handler."""
        start_time = time.time()
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        

        
        # Parse request body for POST
        body_data = {}
        if method == 'POST':
            content_length = self.headers.get('Content-Length')
            if content_length:
                try:
                    body = self.rfile.read(int(content_length)).decode('utf-8')
                    if body:
                        body_data = json.loads(body)
                        # Merge body data into query_params for template rendering
                        for key, value in body_data.items():
                            query_params[key] = [value]
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"[ERROR] Failed to parse request body: {e}")
        
        # Serve static files for frontend
        if method == 'GET' and (path == '/' or path.startswith('/static/')):
            self._serve_static_file(path)
            return
        
        # Special endpoints
        if path == '/__reload' and method == 'POST':
            self._handle_reload()
            latency_ms = int((time.time() - start_time) * 1000)
            self.logger.log(method, path, 200, latency_ms)
            return
        
        if path == '/__logs' and method == 'GET':
            self._handle_logs()
            latency_ms = int((time.time() - start_time) * 1000)
            self.logger.log(method, path, 200, latency_ms)
            return
        

        # Wishlist endpoints with real storage
        if path == '/api/games/wishlist':
            if method == 'GET':
                self._handle_wishlist_get()
                latency_ms = int((time.time() - start_time) * 1000)
                self.logger.log(method, path, 200, latency_ms)
                return
            elif method == 'POST':
                title = query_params.get('title', [''])[0]
                self._handle_wishlist_add(title)
                latency_ms = int((time.time() - start_time) * 1000)
                self.logger.log(method, path, 200, latency_ms)
                return
            elif method == 'DELETE':
                title = query_params.get('title', [''])[0]
                self._handle_wishlist_remove(title)
                latency_ms = int((time.time() - start_time) * 1000)
                self.logger.log(method, path, 200, latency_ms)
                return
        
        # Games CRUD endpoints with real database modification
        if path == '/api/games':
            if method == 'POST':
                self._handle_game_create(body_data)
                latency_ms = int((time.time() - start_time) * 1000)
                self.logger.log(method, path, 201, latency_ms)
                return
            elif method == 'DELETE':
                self._handle_game_delete(query_params)
                latency_ms = int((time.time() - start_time) * 1000)
                self.logger.log(method, path, 200, latency_ms)
                return
        

        # Find endpoint configuration
        endpoint = self.config.find_endpoint(path, method)
        
        if not endpoint:
            self._send_error_response(404, "Endpoint not found")
            latency_ms = int((time.time() - start_time) * 1000)
            self.logger.log(method, path, 404, latency_ms)
            return
        
        # Simulate latency
        latency = endpoint.get('latency_ms', 0)
        if latency > 0:
            time.sleep(latency / 1000.0)
        
        # Simulate failures
        failure_rate = endpoint.get('failure_rate', 0.0)
        if random.random() < failure_rate:
            self._send_error_response(500, "Simulated failure")
            latency_ms = int((time.time() - start_time) * 1000)
            self.logger.log(method, path, 500, latency_ms)
            return
        
        # Render response with templates
        response_data = endpoint.get('response', {})
        rendered_data = TemplateEngine.render(response_data, query_params, self.config)
        
        # Send response
        status = endpoint.get('status', 200)
        self._send_json_response(status, rendered_data)
        
        latency_ms = int((time.time() - start_time) * 1000)
        self.logger.log(method, path, status, latency_ms)
    
    def _handle_reload(self):
        """Reload configuration."""
        self.config.load()
        self._send_json_response(200, {"message": "Configuration reloaded"})
    
    def _handle_logs(self):
        """Return request logs."""
        logs = self.logger.get_logs()
        self._send_json_response(200, {"logs": logs, "count": len(logs)})
    
    def _handle_wishlist_get(self):
        """Get all wishlist items."""
        items = self.wishlist_manager.get_all()
        response = {
            "wishlist": items,
            "total_items": self.wishlist_manager.count(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self._send_json_response(200, response)
    
    def _handle_wishlist_add(self, title):
        """Add item to wishlist."""
        if not title:
            self._send_json_response(400, {"error": "Title is required"})
            return
        
        success, message = self.wishlist_manager.add(title)
        response = {
            "message": message,
            "game_title": title,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "wishlist_count": self.wishlist_manager.count(),
            "success": success
        }
        status = 200 if success else 409  # 409 Conflict if already exists
        self._send_json_response(status, response)
    
    def _handle_wishlist_remove(self, title):
        """Remove item from wishlist."""
        if not title:
            self._send_json_response(400, {"error": "Title is required"})
            return
        
        success, message = self.wishlist_manager.remove(title)
        response = {
            "message": message,
            "game_title": title,
            "removed_at": datetime.now(timezone.utc).isoformat(),
            "wishlist_count": self.wishlist_manager.count(),
            "success": success
        }
        status = 200 if success else 404  # 404 Not Found if doesn't exist
        self._send_json_response(status, response)
    
    def _handle_game_create(self, body_data):
        """Create a new game in the database."""
        if not body_data or 'title' not in body_data:
            self._send_json_response(400, {"error": "Game data with title is required"})
            return
        
        # Add timestamp if not provided
        if 'created_at' not in body_data:
            body_data['created_at'] = datetime.now(timezone.utc).isoformat()
        
        success, result = self.config.add_game(body_data)
        
        if success:
            response = {
                "message": "Game created successfully",
                "game": result,
                "created_at": body_data['created_at'],
                "status": "success"
            }
            self._send_json_response(201, response)
        else:
            self._send_json_response(409, {"error": result, "status": "failed"})
    
    def _handle_game_delete(self, query_params):
        """Delete a game from the database."""
        title = query_params.get('title', [''])[0]
        game_id = query_params.get('id', [''])[0]
        
        if not title and not game_id:
            self._send_json_response(400, {"error": "Game title or id is required"})
            return
        
        # Try to delete by title first, then by id
        identifier_field = 'title' if title else 'id'
        identifier_value = title if title else game_id
        
        success, deleted_game = self.config.delete_game(identifier_field, identifier_value)
        
        if success:
            response = {
                "message": "Game deleted successfully",
                "game": deleted_game,
                "deleted_at": datetime.now(timezone.utc).isoformat(),
                "status": "success"
            }
            self._send_json_response(200, response)
        else:
            self._send_json_response(404, {
                "error": f"Game not found with {identifier_field}: {identifier_value}",
                "status": "failed"
            })
    

    def _send_json_response(self, status, data):
        """Send JSON response with CORS headers."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        
        if self.config.get('cors', True):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error_response(self, status, message):
        """Send error response."""
        self._send_json_response(status, {"error": message})
    
    def _serve_static_file(self, path):
        """Serve static files from public directory."""
        # Map root to index.html
        if path == '/':
            path = '/index.html'
        
        # Build file path
        file_path = os.path.join('public', path.lstrip('/'))
        
        # Security check - prevent directory traversal
        if '..' in file_path:
            self.send_error(403, "Forbidden")
            return
        
        # Check if file exists
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            self.send_error(404, "File not found")
            return
        
        # Determine content type
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # Send file
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            
            if self.config.get('cors', True):
                self.send_header('Access-Control-Allow-Origin', '*')
            
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Local API Mock Server')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--port', type=int, help='Server port (overrides config)')
    args = parser.parse_args()
    
    # Initialize configuration, logger, and wishlist manager
    config = MockServerConfig(args.config)
    logger = RequestLogger()
    wishlist_manager = WishlistManager()
    
    # Set class variables
    MockRequestHandler.config = config
    MockRequestHandler.logger = logger
    MockRequestHandler.wishlist_manager = wishlist_manager
    
    # Determine port
    port = args.port or config.get('port', 8000)
    
    # Start server
    server = HTTPServer(('', port), MockRequestHandler)
    print(f"Mock Server running on http://localhost:{port}")
    print(f"Config: {args.config}")
    print(f"Reload: POST http://localhost:{port}/__reload")
    print(f"Logs: GET http://localhost:{port}/__logs")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Shutting down...")
        server.shutdown()


if __name__ == '__main__':
    main()
