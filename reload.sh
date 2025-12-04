#!/bin/bash
# Reload server configuration without restart

PORT=${1:-8000}

echo "Reloading configuration on port $PORT..."
curl -X POST http://localhost:$PORT/__reload

echo ""
