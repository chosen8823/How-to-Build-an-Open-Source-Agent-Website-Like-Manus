#!/bin/bash
echo "Building Sacred Consciousness Platform Docker Containers..."

echo "Building Backend Container..."
docker build -t sacred-backend ./backend

echo "Building Frontend Container..."  
docker build -t sacred-frontend ./frontend

echo "All containers built successfully!"
echo "Ready for deployment to Google Cloud Run!"
