# Learning Guide: Local API Mock Server

## Core Concepts

### 1. HTTP Server Basics
- **http.server module**: Python's built-in HTTP server framework
- **BaseHTTPRequestHandler**: Base class for handling HTTP requests
- **HTTPServer**: Creates a socket server that listens for HTTP requests

### 2. Threading and Concurrency
- **Thread Safety**: Using locks to protect shared data (config, logs)
- **Concurrent Requests**: Server handles multiple requests using threading
- **Race Conditions**: Why we need `threading.Lock()` for shared state

### 3. Resilience Testing
- **Latency Simulation**: `time.sleep()` to simulate slow networks
- **Failure Injection**: Random failures to test error handling
- **Flaky Services**: Testing retry logic and circuit breakers

### 4. API Design Patterns
- **Configuration as Code**: JSON-based endpoint definitions
- **Hot Reload**: Update config without restarting server
- **Special Endpoints**: `__reload`, `__logs` for server management

## Exercises

### Beginner
1. Add a new endpoint to `config.json`
2. Create a template variable for `{{date}}` (just the date, not time)
3. Add request body logging

### Intermediate
1. Implement request body validation
2. Add support for custom response headers per endpoint
3. Create a CLI command to generate config from OpenAPI spec

### Advanced
1. Implement the full record-and-replay proxy
2. Add WebSocket support
3. Create a web UI for managing endpoints
4. Add authentication simulation (JWT tokens)

## Key Files

- `mock_server.py`: Main server implementation
- `config.json`: Endpoint configuration
- `recorder.py`: Traffic recording (stretch goal)
- `test_server.py`: Integration tests

## Common Patterns

### Adding a New Template Variable
```python
# In TemplateEngine._render_string()
template = re.sub(
    r'\{\{your_variable\}\}',
    'your_value',
    template
)
```

### Adding a New HTTP Method
```python
# In MockRequestHandler
def do_PATCH(self):
    self._handle_request('PATCH')
```

### Configuring Endpoint Behavior
```json
{
  "path": "/api/endpoint",
  "method": "GET",
  "response": {"data": "value"},
  "status": 200,
  "latency_ms": 100,
  "failure_rate": 0.1
}
```

## Limitations and Trade-offs

1. **Single Process**: Not suitable for high-load testing
2. **No State**: Each request is independent (no session management)
3. **Simple Templates**: Not a full template engine like Jinja2
4. **No Request Matching**: Only exact path matches (no wildcards)

## Extension Ideas

- Add request/response middleware
- Support for GraphQL endpoints
- Rate limiting simulation
- Response caching
- Metrics and monitoring dashboard
- Docker container for easy deployment
