# 🚀 Getting Started - Copy & Paste Commands

Quick copy-paste commands to get the application running immediately.

---

## ⚡ FASTEST PATH (2 Steps, 5 minutes)

### Step 1: Run Setup Script
```bash
cd d:\project3
setup.bat
```

Wait 1-2 minutes for Docker to build and start services.

### Step 2: Open in Browser
```
http://localhost:3000
```

**Login with:**
- Username: `admin`
- Password: `admin123`

✅ **Done! You're in the application.**

---

## 📋 Alternative: Manual Setup

### Backend Setup
```bash
cd d:\project3\backend

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create and seed database
python seed.py

# Run Flask server
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL + C to quit
```

### Frontend Setup (New Terminal)
```bash
cd d:\project3\frontend

# Install dependencies
npm install

# Start React development server
npm start
```

Expected output:
```
Compiled successfully!
You can now view the app in the browser.
http://localhost:3000
```

---

## 🔍 First Things to Try

### 1. Admin Dashboard (Advanced Analytics)
1. Login as admin
2. View dashboard with:
   - Total students: 5
   - Total predictions: 0
   - Average GPA: ~3.4
   - Risk distribution chart

### 2. Student Performance
1. Login as `22egit111` / `student123`
2. Click "Generate Prediction" button
3. View:
   - Predicted GPA
   - Risk level
   - Performance factors
   - Recommendations

### 3. Test API Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"

# Use token in next requests
curl http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## 📂 Important Files to Know

```
Backend:           d:\project3\backend\app.py
Frontend:          d:\project3\frontend\src\App.js
ML Model:          d:\project3\ml_model\predictor.py
Database Schema:   d:\project3\database\init.sql
Docker Config:     d:\project3\docker-compose.yml

Documentation:
- Quick Start:     d:\project3\QUICK_START.md
- API Docs:        d:\project3\API_DOCUMENTATION.md
- Deployment:      d:\project3\DEPLOYMENT.md
```

---

## 🆘 Troubleshooting Commands

### Port 5000/3000 Already in Use
```bash
# Find process using port
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Docker Issues
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild everything
docker-compose down
docker-compose up --build
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps

# Recreate everything
docker-compose down -v
docker-compose up -d
```

### Can't Login
```bash
# Seed database again
cd backend
python seed.py
```

---

## 📊 Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Student 1 | `22egit111` | `student123` |
| Student 2 | `22egit112` | `student123` |
| Student 3 | `22egit113` | `student123` |
| Student 4 | `22egit114` | `student123` |
| Student 5 | `22egit115` | `student123` |

---

## 🔗 Quick Links

| Page | URL |
|------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:5000 |
| API Health | http://localhost:5000/api/health |
| Admin Login | http://localhost:3000/login |

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Frontend loads at http://localhost:3000
- [ ] Can login with admin/admin123
- [ ] Admin dashboard shows data
- [ ] Can login as student 22egit111
- [ ] Can see student dashboard
- [ ] Can generate predictions
- [ ] Backend API responds: http://localhost:5000/api/health

---

## 📖 Full Documentation

Start reading here if you want more details:
1. INDEX.md - Documentation hub
2. SUMMARY.md - Project overview
3. README.md - Full documentation
4. QUICK_START.md - Detailed setup guide
5. API_DOCUMENTATION.md - API reference

---

## 🎯 Common Tasks

### View Application Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### See Running Services
```bash
docker ps
```

### Open Database Shell
```bash
docker exec -it postgres psql -U student_user -d student_performance
```

### Stop All Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild Everything
```bash
docker-compose down -v
docker-compose up --build
```

---

## 💻 System Requirements

- Docker Desktop (for easy setup)
- OR Python 3.11+ and Node.js 18+ (for manual)
- PostgreSQL 15 (if not using Docker)
- 4GB RAM minimum
- 2GB disk space

---

## 🚀 You're All Set!

**Next:** 
1. Run `setup.bat`
2. Open http://localhost:3000
3. Login with admin / admin123
4. Explore the application!

**Questions?** See INDEX.md for documentation links.

---

## 📝 Notes

- All credentials are for development only
- Change JWT_SECRET_KEY before production
- Database is automatically created and seeded
- Test data includes 5 students with academic records
- ML models are pre-trained with sample data

---

**Happy predicting! 🎓**
