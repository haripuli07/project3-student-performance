# Quick Start Guide

## 🚀 Installation & Setup (5 minutes)

### Option 1: Docker (Recommended)

**Windows:**
```bash
cd d:\project3
setup.bat
```

**Mac/Linux:**
```bash
cd project3
bash setup.sh
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows or source venv/bin/activate
pip install -r requirements.txt
python seed.py
python app.py
```

**Frontend (New Terminal):**
```bash
cd frontend
npm install
npm start
```

**Expected Output:**
- Backend: Running at `http://localhost:5000`
- Frontend: Running at `http://localhost:3000`

---

## 📝 First Login

### Admin Account
```
Email: admin@excel.edu
Username: admin
Password: admin123
```

### Student Accounts
```
Username: 22egit111 - 22egit115
Password: student123
```

Access: http://localhost:3000

---

## 🎯 What to Do First

### 1. Check Admin Dashboard
1. Login with admin credentials
2. View → **Dashboard**
   - 5 total students
   - Student performance metrics
   - Risk distribution chart
   - At-risk students list

### 2. Login as Student
1. Logout and login with `22egit111 / student123`
2. View → **Student Dashboard**
   - Personal performance analysis
   - Generate new prediction
   - View recommendations
   - Track academic records

### 3. Generate ML Prediction
- Click "Generate Prediction" button
- View predicted GPA
- Check risk level
- Read personalized recommendations

---

## 📊 Key Features to Explore

### Admin Dashboard Features
```
Dashboard Tab:
├── Key Metrics (Total Students, Predictions, Avg GPA)
├── Risk Distribution (Pie Chart)
├── Top Performers (Ranked List)
└── At-Risk Students (Intervention Recommendations)
```

### Student Dashboard Features
```
Student Tab:
├── Performance Analysis
│   ├── Predicted GPA
│   └── Risk Level
├── Performance Factors
│   ├── Attendance Status
│   ├── Academic Trend
│   └── Assessment Balance
├── Recommendations
│   └── Personalized Tips
└── Academic Records
    └── Subject-wise Grades
```

---

## 🛠️ API Testing

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Admin Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Get Dashboard
```bash
curl http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📂 Project Files

**Important Files to Know:**

```
Backend API:
- backend/app.py         → Main Flask app
- backend/models.py      → Database models
- backend/routes/*.py    → API endpoints

Frontend UI:
- frontend/src/App.js              → Main component
- frontend/src/pages/*.js          → Page components
- frontend/src/store/authStore.js  → Auth logic

ML Engine:
- ml_model/predictor.py  → ML prediction engine
- ml_model/models/*.pkl  → Trained models

Database:
- database/init.sql      → Database schema
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Can't Connect to Backend
- Verify backend is running: `http://localhost:5000/api/health`
- Check REACT_APP_API_URL in frontend/.env
- Restart both services

### Database Issues
```bash
# Using Docker Compose
docker-compose down
docker-compose up -d --build

# Local PostgreSQL
# Ensure PostgreSQL service is running
# Recreate database or run seed.py again
```

### Port Conflicts (Docker)
Edit `docker-compose.yml` to use different ports
```yaml
ports:
  - "5001:5000"  # Backend
  - "3001:3000"  # Frontend
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| README.md | Project overview & features |
| DEPLOYMENT.md | Production deployment guide |
| API_DOCUMENTATION.md | Complete API reference |
| PROJECT_STRUCTURE.md | File structure & architecture |
| This File | Quick start guide |

---

## 🎓 Understanding the ML Model

### How Predictions Work

1. **Data Collection**
   - Student's past GPA
   - Attendance percentage
   - Internal & external marks
   - Number of subjects

2. **Feature Processing**
   - Normalize data
   - Calculate averages
   - Apply statistical scaling

3. **Model Prediction**
   - Gradient Boosting → Predict GPA
   - Random Forest → Classify Risk Level
   - Generate factors & recommendations

4. **Output**
   - Predicted GPA
   - Risk Level (Low/Medium/High)
   - Influencing Factors
   - Actionable Recommendations

### Risk Levels

| Level | GPA | Attendance | Status |
|-------|-----|-----------|--------|
| Low | > 3.5 | > 85% | Excellent |
| Medium | 2.5-3.5 | 75-85% | Needs Attention |
| High | < 2.5 | < 75% | Requires Help |

---

## 🔑 Key Endpoints

### Authentication
```
POST   /api/auth/login
POST   /api/auth/register
GET    /api/auth/me
```

### Student Data
```
GET    /api/students
GET    /api/students/:id
POST   /api/students/:id/academic
POST   /api/students/:id/attendance
```

### Predictions
```
GET    /api/predictions/predict/:id
GET    /api/predictions/history/:id
GET    /api/predictions/all
```

### Admin Analytics
```
GET    /api/admin/dashboard
GET    /api/admin/analytics/risk-distribution
GET    /api/admin/analytics/top-performers
GET    /api/admin/analytics/at-risk-students
```

---

## 💡 Next Steps

1. **Add More Student Data**
   - Edit `backend/seed.py` to add more students
   - Run seed.py to populate database

2. **Customize ML Model**
   - Modify `ml_model/predictor.py`
   - Retrain models with your data
   - Adjust recommendation logic

3. **Deploy to Production**
   - See DEPLOYMENT.md
   - Configure production database
   - Set up security (HTTPS, secrets)

4. **Add Features**
   - Email notifications
   - Export reports
   - Advanced analytics
   - Mobile app

---

## 📱 System Requirements

- **CPU**: 2+ cores
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space
- **Network**: Internet connection (for npm/pip packages)

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Cannot connect to API" | Check backend at http://localhost:5000 |
| "Database connection failed" | Ensure PostgreSQL is running, check .env |
| "npm install fails" | Delete node_modules, clear npm cache, retry |
| "Port 5000/3000 in use" | Use different ports in docker-compose.yml |
| "Login fails" | Run `python seed.py` to create test users |

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Backend running at http://localhost:5000
- [ ] Frontend running at http://localhost:3000
- [ ] Database connected (check backend logs)
- [ ] Can login with admin/admin123
- [ ] Dashboard loads with data
- [ ] Can generate prediction for student
- [ ] Admin analytics working

---

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review API_DOCUMENTATION.md for endpoint details
3. Check application logs: `docker-compose logs -f`
4. Review error messages in browser console

---

## 🎉 You're Ready!

The application is now ready to use. Explore the features, test the ML predictions, and administer the student performance system!

**Happy predicting! 🚀**
