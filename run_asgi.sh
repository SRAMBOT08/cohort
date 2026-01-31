#!/bin/bash
# Run Django with ASGI (Daphne)

echo "Starting Django with ASGI support..."
cd backend
daphne -b 0.0.0.0 -p 8000 config.asgi:application
