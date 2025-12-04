# Limitations and Constraints

## Technical Limitations

### 1. Concurrency
- **Single Process:** Uses Python's built-in `http.server` which is single-process
- **GIL Constraint:** Python's Global Interpreter Lock limits true parallelism
- **Thread Per Request:** Each request spawns a thread, but CPU-bound operations are serialized
- **Not Production-Ready:** Not suitable for high-load or production environments

**Impact:** Limited concurrent request handling capacity

**Workaround:** Use for local testing only, not load testing

### 2. State Management
- **Stateless:** No session management or state persistence
- **No Database Writes:** Database is read-only from JSON file
- **No Request History:** Only last 100 requests logged (circular buffer)
- **Memory Only:** All data stored in RAM, lost on restart

**Impact:** Cannot simulate stateful APIs or track user sessions

**Workaround:** Use external state management if needed

### 3. Request Matching
- **Exact Path Only:** No wildcard or regex path matching
- **No Path Parameters:** Cannot match `/api/users/:id` patterns
- **No Content Negotiation:** Always returns JSON
- **No Request Body Validation:** Accepts any POST/PUT body

**Impact:** Limited flexibility in endpoint definition

**Workaround:** Define each endpoint explicitly

### 4. Template Engine
- **Simple Patterns Only:** Not a full template engine like Jinja2
- **No Conditionals:** Cannot use if/else logic in templates
- **No Loops:** Cannot iterate in templates
- **No Nested Queries:** Limited database query capabilities

**Impact:** Complex response logic requires code changes

**Workaround:** Pre-compute complex responses or extend template engine

### 5. Security
- **No Authentication:** No user authentication or authorization
- **No Input Validation:** Trusts all input data
- **No Rate Limiting:** Can be overwhelmed by requests
- **CORS Wide Open:** Allows all origins by default
- **No HTTPS:** HTTP only, no SSL/TLS support

**Impact:** Not suitable for any production or public-facing use

**Workaround:** Use only in trusted local environments

### 6. Data Handling
- **JSON Only:** Only supports JSON request/response bodies
- **No File Uploads:** Cannot handle multipart/form-data
- **No Streaming:** Entire response loaded in memory
- **Limited Database:** Simple list-based filtering only

**Impact:** Cannot simulate file upload APIs or streaming responses

**Workaround:** Use specialized tools for these scenarios

### 7. Error Handling
- **Basic Error Responses:** Simple error messages only
- **No Custom Error Formats:** Cannot customize error response structure
- **No Error Recovery:** Server may crash on unexpected errors
- **Limited Logging:** Basic request logging only

**Impact:** Debugging complex issues may be difficult

**Workaround:** Add custom error handling as needed

## Functional Limitations

### 1. Traffic Recording
- **Incomplete Implementation:** Record mode requires manual setup
- **No Proxy Support:** Cannot automatically proxy to real servers
- **Manual Recording:** Must manually create recording files

**Impact:** Cannot easily record real API traffic

**Workaround:** Use tools like Charles Proxy or mitmproxy

### 2. Configuration
- **No Hot Schema Validation:** Schema not validated on reload
- **No Config Inheritance:** Cannot extend or compose configs
- **No Environment Variables:** Cannot use env vars in config
- **JSON Only:** No YAML or other format support

**Impact:** Configuration management can be tedious

**Workaround:** Use external tools to generate configs

### 3. Response Generation
- **No Response Schemas:** Cannot validate response against schema
- **No Faker Integration:** No built-in fake data generation
- **Static Templates:** Templates evaluated once per request
- **No Response Variants:** Cannot A/B test different responses

**Impact:** Limited dynamic response capabilities

**Workaround:** Pre-generate varied responses or extend template engine

### 4. Testing Support
- **No Built-in Assertions:** Cannot verify request expectations
- **No Request Matching:** Cannot assert specific requests were made
- **No Mock Verification:** Cannot verify mock was called correctly
- **Manual Testing:** Requires external test framework

**Impact:** Cannot use as a test double with verification

**Workaround:** Use with external testing frameworks

## Performance Limitations

### 1. Throughput
- **Low RPS:** Limited requests per second capacity
- **No Connection Pooling:** Each request creates new connection
- **No Keep-Alive:** Connections not reused
- **Blocking I/O:** Synchronous request handling

**Benchmark:** ~100-500 RPS on typical hardware

### 2. Latency
- **Simulated Only:** Latency simulation uses `time.sleep()`
- **Blocks Thread:** Simulated latency blocks request thread
- **No Jitter:** Latency is fixed, not variable
- **No Network Simulation:** Cannot simulate packet loss, etc.

**Impact:** Latency simulation is simplistic

### 3. Memory
- **Database in RAM:** Entire database loaded in memory
- **No Pagination:** All records returned at once
- **Log Buffer:** Circular buffer limited to 100 entries
- **No Compression:** Responses not compressed

**Impact:** Large databases may cause memory issues

**Workaround:** Keep database files small (<10MB)

## Comparison with Alternatives

### vs. WireMock
- ❌ No request matching patterns
- ❌ No request verification
- ❌ No stateful scenarios
- ✅ Simpler configuration
- ✅ No JVM required

### vs. json-server
- ❌ No REST conventions
- ❌ No automatic CRUD
- ❌ No database persistence
- ✅ More control over responses
- ✅ Latency and failure simulation

### vs. Mockoon
- ❌ No GUI
- ❌ No OpenAPI import
- ❌ No proxy mode
- ✅ Lightweight
- ✅ Easy to script and automate

### vs. Postman Mock Server
- ❌ No cloud sync
- ❌ No collection-based mocks
- ❌ No team collaboration
- ✅ Fully local
- ✅ No account required

## When to Use This Server

### Good Use Cases ✅
- Local development and testing
- Learning HTTP and API concepts
- Quick prototyping
- Simulating flaky services
- Testing error handling
- Offline development

### Bad Use Cases ❌
- Production environments
- Load testing
- Public-facing APIs
- High-concurrency scenarios
- Complex stateful workflows
- Security-sensitive applications

## Mitigation Strategies

### For Production-Like Testing
Use production-grade mock servers:
- WireMock
- Mockoon
- Prism (OpenAPI)
- Postman Mock Server

### For Load Testing
Use dedicated load testing tools:
- Apache JMeter
- Gatling
- k6
- Locust

### For Complex Scenarios
Use full API frameworks:
- FastAPI (Python)
- Express (Node.js)
- Flask (Python)
- Sinatra (Ruby)

## Known Issues

1. **Config Reload Race Condition:** Rare race condition during hot reload
2. **Large Response Memory:** Large responses may cause memory spikes
3. **Thread Cleanup:** Threads may not clean up properly on shutdown
4. **Error Messages:** Generic error messages not always helpful

## Future Improvements

See [ARCHITECTURE.md](ARCHITECTURE.md) for planned enhancements.
