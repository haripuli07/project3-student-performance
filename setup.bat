@echo off
REM Student Performance Predictor - Setup Script for Windows

echo ==========================================
echo Student Performance Predictor Setup
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

echo ✓ Docker found

REM Create .env files from examples
if not exist "backend\.env" (
    echo Creating backend .env file...
    copy backend\.env.example backend\.env
)

if not exist "frontend\.env" (
    echo Creating frontend .env file...
    copy frontend\.env.example frontend\.env
)

REM Build and start containers
echo Building Docker images...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for services to start...
timeout /t 10

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Default Credentials:
echo Username: admin
echo Password: admin123
echo.
echo Access the application:
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:5000/api
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
