# Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Navigate to project root
cd project3

# Run setup script
# On Windows:
setup.bat

# On Mac/Linux:
bash setup.sh
```

This will:
1. Create necessary `.env` files
2. Build Docker images
3. Start all services (PostgreSQL, Backend, Frontend)
4. Initialize the database

## Manual Deployment

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Deployment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
python seed.py

# Run server
python app.py
```

Backend will start at `http://localhost:5000`

### Frontend Deployment

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start

# Or build for production
npm run build
```

Frontend will start at `http://localhost:3000`

## Database Setup

### Option 1: Automatic (via Docker)
Database is automatically initialized when using Docker Compose.

### Option 2: PostgreSQL

```bash
# Create database
createdb student_performance

# Run schema
psql student_performance < database/init.sql

# Seed test data (optional)
cd backend
python seed.py
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/student_performance
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Production Deployment

### Backend (Gunicorn + Nginx)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Configure Nginx as reverse proxy
```

nginx.conf example:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend (nginx static hosting)

```bash
# Build for production
npm run build

# Serve from nginx
```

nginx.conf:
```nginx
server {
    listen 80;
    server_name your-frontend-domain.com;
    
    root /var/www/student-performance/build;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Docker Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://user:${DB_PASSWORD}@postgres:5432/student_performance
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      FLASK_ENV: production
    restart: always
    depends_on:
      - postgres

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    restart: always

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Health Checks

### Backend Health
```bash
curl http://localhost:5000/api/health
```

### Test Endpoints
```bash
# Admin login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Database Connection Failed
- Check PostgreSQL is running
- Verify DATABASE_URL is correct
- Ensure database exists

### Frontend Can't Connect to API
- Verify REACT_APP_API_URL
- Check backend is running
- Check CORS settings in Flask

### Docker Issues
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild images
docker-compose down
docker-compose up --build
```

## Monitoring

### View Application Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# File logs (if configured)
tail -f logs/app.log
```

## Performance Optimization

1. **Database**: Add indexes (already configured)
2. **Caching**: Implement Redis for frequently accessed data
3. **Frontend**: Use React.memo for component optimization
4. **API**: Implement request throttling

## Security Hardening

1. Change default JWT_SECRET_KEY
2. Enable HTTPS in production
3. Add rate limiting to API
4. Implement CORS whitelist
5. Use environment variables for secrets
6. Regular security updates

## Scaling

For production scaling:
- Use multiple backend instances with load balancer
- Implement database replication
- Use CDN for frontend assets
- Cache API responses with Redis
