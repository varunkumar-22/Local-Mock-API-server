# Architecture Overview

## System Design

The Local Mock API Server is built with a modular architecture that separates concerns and allows for easy extension.

## Core Components

### 1. MockServerConfig
**Location:** `server/mock_server.py`

Manages server configuration with thread-safe access and hot-reload support.

**Responsibilities:**
- Load configuration from JSON files
- Load database files
- Provide thread-safe access to config data
- Filter and query database records

**Key Methods:**
- `load()` - Reload configuration from disk
- `find_endpoint(path, method)` - Match incoming requests to endpoints
- `get_database()` - Access database records
- `filter_database(field, value)` - Filter records by field

### 2. TemplateEngine
**Location:** `server/mock_server.py`

Simple template engine for dynamic response generation.

**Supported Templates:**
- `{{timestamp}}` - Current ISO timestamp
- `{{uuid}}` - Random UUID
- `{{random_int}}` - Random integer
- `{{query.param}}` - Query parameter values
- `{{database}}` - Full database
- `{{database_count}}` - Record count
- `{{database_filter:field:value}}` - Filtered records
- `{{database_find:field:value}}` - Single record lookup
- `{{database_filter_genre:genre}}` - Genre-based filtering

**Design Pattern:** Recursive rendering for nested data structures

### 3. MockRequestHandler
**Location:** `server/mock_server.py`

HTTP request handler that processes incoming requests.

**Request Flow:**
1. Parse URL and query parameters
2. Check for special endpoints (`__reload`, `__logs`)
3. Find matching endpoint configuration
4. Simulate latency (if configured)
5. Simulate failures (if configured)
6. Render response templates
7. Send JSON response with CORS headers
8. Log request details

### 4. RequestLogger
**Location:** `server/mock_server.py`

Thread-safe request logger with circular buffer.

**Features:**
- Stores last 100 requests (configurable)
- Thread-safe operations
- Timestamp, method, path, status, latency tracking

### 5. TrafficRecorder (Stretch Goal)
**Location:** `server/recorder.py`

Records and replays HTTP traffic for testing.

**Modes:**
- **Record Mode:** Proxy requests and save responses
- **Replay Mode:** Serve previously recorded responses

## Data Flow

```
Client Request
    ↓
MockRequestHandler
    ↓
Parse URL & Query Params
    ↓
Find Endpoint Config ← MockServerConfig
    ↓
Simulate Latency
    ↓
Simulate Failures
    ↓
Render Templates ← TemplateEngine
    ↓
Send Response
    ↓
Log Request ← RequestLogger
```

## Threading Model

- **Main Thread:** HTTP server event loop
- **Request Threads:** Each request handled in separate thread
- **Shared State:** Protected by `threading.Lock()`
  - Configuration data
  - Database records
  - Request logs

## Configuration Schema

```json
{
  "port": 8000,
  "cors": true,
  "database": "path/to/database.json",
  "endpoints": [
    {
      "path": "/api/resource",
      "method": "GET|POST|PUT|DELETE|PATCH",
      "response": { /* JSON response */ },
      "status": 200,
      "latency_ms": 100,
      "failure_rate": 0.0
    }
  ]
}
```

## Extension Points

### Adding New Template Variables
Extend `TemplateEngine._render_string()` with new regex patterns.

### Adding New HTTP Methods
Add `do_METHOD()` methods to `MockRequestHandler`.

### Custom Response Logic
Extend `MockRequestHandler._handle_request()` for custom behavior.

### Database Adapters
Extend `MockServerConfig` to support different data sources (SQL, MongoDB, etc.).

## Design Decisions

### Why Python's http.server?
- Built-in, no external dependencies
- Simple and lightweight
- Good for learning HTTP fundamentals
- Sufficient for local testing

### Why JSON Configuration?
- Human-readable and editable
- Easy to version control
- Standard format with schema validation
- No code changes needed for new endpoints

### Why Thread Locks?
- Prevent race conditions in shared state
- Ensure consistent reads during config reload
- Protect log buffer from corruption

### Why Simple Templates?
- No external dependencies
- Fast rendering
- Sufficient for common use cases
- Easy to understand and extend

## Performance Considerations

- **Single Process:** Not suitable for high-load testing
- **Thread Per Request:** Limited by Python GIL
- **In-Memory Database:** Fast but limited by RAM
- **No Caching:** Each request re-renders templates

## Security Considerations

- **No Authentication:** Not for production use
- **No Input Validation:** Trusts all input
- **No Rate Limiting:** Can be overwhelmed
- **CORS Enabled:** Allows all origins

## Future Enhancements

1. **Multi-process support** for better concurrency
2. **WebSocket support** for real-time testing
3. **GraphQL endpoint** support
4. **Request/response middleware** pipeline
5. **Metrics and monitoring** dashboard
6. **Docker container** for easy deployment
