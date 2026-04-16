#!/bin/bash

# Student Performance Predictor - Setup Script

echo "=========================================="
echo "Student Performance Predictor Setup"
echo "=========================================="

# Create .env files from examples
if [ ! -f "backend/.env" ]; then
    echo "Creating backend .env file..."
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend .env file..."
    cp frontend/.env.example frontend/.env
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker found"

# Build and start containers
echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
if docker ps | grep -q "student-performance-frontend"; then
    echo "✓ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend failed to start"
fi

if docker ps | grep -q "student-performance-backend"; then
    echo "✓ Backend is running at http://localhost:5000"
else
    echo "❌ Backend failed to start"
fi

if docker ps | grep -q "postgres"; then
    echo "✓ Database is running"
else
    echo "❌ Database failed to start"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Default Credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Access the application:"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:5000/api"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
