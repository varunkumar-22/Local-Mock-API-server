#!/usr/bin/env python3
"""
Main entry point for Local API Mock Server
"""

import sys
import os
import argparse

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

# Import after path is set
from mock_server import MockServerConfig, MockRequestHandler, RequestLogger, WishlistManager
from http.server import HTTPServer

def main():
    """Main entry point with default config path."""
    parser = argparse.ArgumentParser(description='Local API Mock Server')
    parser.add_argument('--config', default='config/config.json', help='Configuration file path')
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
        print("\n⏹ Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    main()
