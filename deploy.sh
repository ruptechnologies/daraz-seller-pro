#!/bin/bash

# Build Docker image
docker build -t daraz-seller-pro .

# Run container
docker run -d -p 8501:8501 --name daraz-app daraz-seller-pro

echo "Application deployed at http://localhost:8501"