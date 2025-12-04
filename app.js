const API_BASE = 'http://localhost:8000';

const endpoints = {
    'games': {
        method: 'GET',
        url: '/api/games',
        params: []
    },
    'new-releases': {
        method: 'GET',
        url: '/api/games/new-releases',
        params: []
    },
    'highest-rated': {
        method: 'GET',
        url: '/api/games/highest-rated',
        params: []
    },
    'discounts': {
        method: 'GET',
        url: '/api/games/discounts',
        params: []
    },
    'search': {
        method: 'GET',
        url: '/api/games/search',
        params: [{ name: 'title', placeholder: 'e.g., Minecraft', required: true }]
    },
    'genre': {
        method: 'GET',
        url: '/api/games/genre',
        params: [{ name: 'genre', placeholder: 'e.g., RPG, FPS, Horror', required: true }]
    },
    'review': {
        method: 'POST',
        url: '/api/games/review',
        params: [
            { name: 'title', placeholder: 'Game title', required: true },
            { name: 'review', placeholder: 'Write your review here...', required: true, type: 'textarea' }
        ]
    },
    'wishlist': {
        method: 'GET',
        url: '/api/games/wishlist',
        params: []
    },
    'wishlist-add': {
        method: 'POST',
        url: '/api/games/wishlist',
        params: [{ name: 'title', placeholder: 'Game title', required: true }]
    },
    'wishlist-remove': {
        method: 'DELETE',
        url: '/api/games/wishlist',
        params: [{ name: 'title', placeholder: 'Game title', required: true }]
    },
    'health': {
        method: 'GET',
        url: '/api/health',
        params: []
    },
    'logs': {
        method: 'GET',
        url: '/__logs',
        params: []
    },
    'reload': {
        method: 'POST',
        url: '/__reload',
        params: []
    }
};

let currentEndpoint = 'games';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkServerStatus();
    setupEventListeners();
    loadEndpoint('games');
});

function setupEventListeners() {
    // Endpoint buttons
    document.querySelectorAll('.endpoint-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const endpoint = btn.dataset.endpoint;
            loadEndpoint(endpoint);
        });
    });

    // Send request button
    document.getElementById('send-request').addEventListener('click', sendRequest);
}

function loadEndpoint(endpointKey) {
    currentEndpoint = endpointKey;
    const endpoint = endpoints[endpointKey];
    
    // Update active button
    document.querySelectorAll('.endpoint-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.endpoint === endpointKey);
    });
    
    // Update method badge
    const methodBadge = document.getElementById('request-method');
    methodBadge.textContent = endpoint.method;
    methodBadge.className = `method-badge ${endpoint.method}`;
    
    // Update URL
    document.getElementById('request-url').value = API_BASE + endpoint.url;
    
    // Show/hide params section
    const paramsSection = document.getElementById('params-section');
    const paramsContainer = document.getElementById('params-container');
    
    if (endpoint.params.length > 0) {
        paramsSection.style.display = 'block';
        paramsContainer.innerHTML = endpoint.params.map(param => {
            if (param.type === 'textarea') {
                return `
                    <div class="param-input">
                        <label>${param.name}${param.required ? '*' : ''}:</label>
                        <textarea 
                            id="param-${param.name}" 
                            placeholder="${param.placeholder}"
                            ${param.required ? 'required' : ''}
                            rows="4"
                        ></textarea>
                    </div>
                `;
            } else {
                return `
                    <div class="param-input">
                        <label>${param.name}${param.required ? '*' : ''}:</label>
                        <input 
                            type="text" 
                            id="param-${param.name}" 
                            placeholder="${param.placeholder}"
                            ${param.required ? 'required' : ''}
                        >
                    </div>
                `;
            }
        }).join('');
    } else {
        paramsSection.style.display = 'none';
        paramsContainer.innerHTML = '';
    }
    
    // Show/hide body section
    const bodySection = document.getElementById('body-section');
    const bodyTextarea = document.getElementById('request-body');
    
    if (endpoint.hasBody) {
        bodySection.style.display = 'block';
        bodyTextarea.value = JSON.stringify(endpoint.bodyExample || {}, null, 2);
    } else {
        bodySection.style.display = 'none';
        bodyTextarea.value = '';
    }
    
    // Clear response
    document.getElementById('response-content').innerHTML = '<p class="placeholder">Click "Send Request" to see the response</p>';
    document.getElementById('response-status').textContent = '';
    document.getElementById('response-time').textContent = '';
}

async function sendRequest() {
    const endpoint = endpoints[currentEndpoint];
    const btn = document.getElementById('send-request');
    
    // Build URL with params - use query params for all methods for simplicity
    let url = API_BASE + endpoint.url;
    const params = new URLSearchParams();
    
    for (const param of endpoint.params) {
        const value = document.getElementById(`param-${param.name}`)?.value;
        if (param.required && !value) {
            showError(`Parameter "${param.name}" is required`);
            return;
        }
        if (value) {
            params.append(param.name, value);
        }
    }
    
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    // Update UI
    btn.disabled = true;
    btn.textContent = 'Sending...';
    document.getElementById('response-content').innerHTML = '<p class="placeholder">Loading...</p>';
    
    const startTime = performance.now();
    
    try {
        const fetchOptions = {
            method: endpoint.method,
            mode: 'cors'
        };
        
        // Add body for POST requests
        if (endpoint.hasBody) {
            const bodyText = document.getElementById('request-body').value;
            if (bodyText.trim()) {
                try {
                    // Validate JSON
                    const bodyData = JSON.parse(bodyText);
                    fetchOptions.body = JSON.stringify(bodyData);
                    fetchOptions.headers = {
                        'Content-Type': 'application/json'
                    };
                } catch (jsonError) {
                    showError(`Invalid JSON in request body: ${jsonError.message}`);
                    btn.disabled = false;
                    btn.textContent = 'Send Request';
                    return;
                }
            }
        }
        
        console.log('Sending request:', url, fetchOptions);
        
        const response = await fetch(url, fetchOptions);
        
        console.log('Response received:', response.status, response.statusText);
        
        const endTime = performance.now();
        const duration = Math.round(endTime - startTime);
        
        // Check if response is ok
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        // Get response text first to debug JSON issues
        const responseText = await response.text();
        console.log('Response text:', responseText);
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (jsonError) {
            console.error('JSON parse error:', jsonError);
            console.error('Response was:', responseText);
            throw new Error(`Invalid JSON response: ${jsonError.message}`);
        }
        
        console.log('Response data:', data);
        
        // Update response UI
        document.getElementById('response-status').textContent = `Status: ${response.status}`;
        document.getElementById('response-status').className = `status-${response.status}`;
        document.getElementById('response-time').textContent = `${duration}ms`;
        
        document.getElementById('response-content').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        
    } catch (error) {
        console.error('Request error:', error);
        showError(`Request failed: ${error.message}`);
        document.getElementById('response-status').textContent = 'Error';
        document.getElementById('response-status').className = 'status-500';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Send Request';
    }
}

async function checkServerStatus() {
    const statusDot = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    try {
        const response = await fetch(`${API_BASE}/api/health`, {
            method: 'GET',
            signal: AbortSignal.timeout(3000)
        });
        
        if (response.ok) {
            statusDot.classList.add('online');
            statusText.textContent = 'Server Online';
        } else {
            statusDot.classList.add('offline');
            statusText.textContent = 'Server Error';
        }
    } catch (error) {
        statusDot.classList.add('offline');
        statusText.textContent = 'Server Offline';
    }
    
    // Check again in 10 seconds
    setTimeout(checkServerStatus, 10000);
}

function showError(message) {
    document.getElementById('response-content').innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
}
