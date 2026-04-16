# Project Structure Overview

```
project3/
│
├── 📁 backend/                          # Flask Backend API
│   ├── app.py                          # Main Flask application
│   ├── models.py                       # SQLAlchemy database models
│   ├── seed.py                         # Database seeding script
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Docker configuration
│   ├── .env.example                    # Environment template
│   ├── .gitignore                      # Git ignore patterns
│   └── 📁 routes/                      # API route handlers
│       ├── __init__.py
│       ├── auth.py                     # Authentication endpoints
│       ├── students.py                 # Student management
│       ├── predictions.py              # ML predictions
│       └── admin.py                    # Admin analytics
│
├── 📁 frontend/                         # React Frontend Application
│   ├── package.json                    # Node dependencies
│   ├── Dockerfile                      # Docker configuration
│   ├── .env.example                    # Environment template
│   ├── .gitignore                      # Git ignore patterns
│   ├── 📁 public/
│   │   └── index.html                  # HTML entry point
│   └── 📁 src/
│       ├── App.js                      # Main app component
│       ├── App.css                     # Styling
│       ├── index.js                    # React entry point
│       ├── 📁 components/              # Reusable components
│       │   ├── Navbar.js              # Navigation bar
│       │   └── PrivateRoute.js        # Route protection
│       ├── 📁 pages/                   # Page components
│       │   ├── LoginPage.js           # Login page
│       │   ├── AdminDashboard.js      # Admin dashboard
│       │   └── StudentDashboard.js    # Student dashboard
│       ├── 📁 store/                   # State management
│       │   └── authStore.js           # Zustand auth store
│       └── 📁 utils/                   # Utility functions
│           └── api.js                  # API endpoints
│
├── 📁 ml_model/                         # Machine Learning Module
│   ├── predictor.py                    # ML prediction engine
│   ├── requirements.txt                # ML dependencies
│   └── 📁 models/                      # Trained models storage
│       ├── gpa_predictor.pkl          # GPA prediction model
│       ├── risk_classifier.pkl        # Risk classification model
│       └── scaler.pkl                 # Data scaler
│
├── 📁 database/                         # Database Configuration
│   └── init.sql                        # Database schema & indexes
│
├── 📄 docker-compose.yml                # Docker Compose configuration
├── 📄 .gitignore                        # Root gitignore
├── 📄 README.md                         # Project README
├── 📄 DEPLOYMENT.md                     # Deployment guide
├── 📄 API_DOCUMENTATION.md              # API reference
├── 📄 setup.sh                          # Unix/Mac setup script
└── 📄 setup.bat                         # Windows setup script
```

# Key Files Description

## Backend Files

### app.py
- Flask application initialization
- Database configuration
- JWT setup
- Blueprint registration
- Health check endpoint

### models.py
- User model (authentication)
- Student model (student information)
- AcademicRecord model (grades/scores)
- Attendance model (attendance tracking)
- Prediction model (ML predictions)
- Administrator model (admin users)

### routes/auth.py
- User registration
- Login/logout
- Get current user
- Change password

### routes/students.py
- Get all students (admin)
- Get student details
- Add academic records
- Add attendance records

### routes/predictions.py
- Generate performance prediction
- Get prediction history
- Get all predictions (admin)
- Feature extraction

### routes/admin.py
- Dashboard analytics
- User management
- Risk distribution analytics
- Top performers list
- At-risk students detection

## Frontend Files

### App.js
- Main app component
- Route definitions
- Protected routes setup
- Navigation logic

### pages/LoginPage.js
- Login form
- Authentication handling
- Role-based navigation
- Error handling

### pages/AdminDashboard.js
- Key metrics display
- Risk distribution chart
- Top performers list
- At-risk students table
- Analytics visualization

### pages/StudentDashboard.js
- Student profile display
- Performance prediction
- Risk level visualization
- Recommendations
- Academic records table

### store/authStore.js
- Zustand auth state management
- Login/logout logic
- Token management
- User data storage

## ML Module Files

### predictor.py
- PerformancePredictor class
- Model initialization
- GPA prediction
- Risk classification
- Factor analysis
- Recommendation generation
- Model training/retraining

## Database Files

### init.sql
- Users table
- Students table
- Academic records table
- Attendance table
- Predictions table
- Administrators table
- Indexes for performance
```

# Technology Stack

## Backend
- **Framework**: Flask 2.3.0
- **ORM**: SQLAlchemy 3.0.0
- **Authentication**: Flask-JWT-Extended 4.4.4
- **Core ML**: scikit-learn 1.3.0
- **Data Processing**: pandas, numpy
- **Password Hashing**: bcrypt

## Frontend
- **Library**: React 18.2.0
- **Routing**: React Router 6.14.0
- **State**: Zustand 4.3.9
- **HTTP**: Axios 1.4.0
- **Styling**: Tailwind CSS 3.3.0
- **Charts**: Chart.js + react-chartjs-2
- **Icons**: React Icons 4.10.1

## Database
- **Primary**: PostgreSQL 15
- **Data Type**: JSONB for flexible storage

## DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Python**: 3.11
- **Node.js**: 18 Alpine

# Features Overview

## 1. Authentication System
✓ User registration with role selection
✓ Secure login with JWT tokens
✓ Password hashing with bcrypt
✓ Role-based access control (Admin, Teacher, Student)
✓ Password change functionality

## 2. Student Management
✓ Student profile with admission details
✓ Academic record tracking
✓ Attendance monitoring
✓ Personal dashboard
✓ Performance history

## 3. Machine Learning Predictions
✓ GPA prediction using Gradient Boosting
✓ Risk classification (Low, Medium, High)
✓ Factor analysis (attendance, performance trends, assessment balance)
✓ Personalized recommendations
✓ Model retraining capability

## 4. Admin Controls
✓ Dashboard with key metrics
✓ Risk distribution analytics
✓ Top performers identification
✓ At-risk students monitoring
✓ User management (enable/disable)
✓ Role assignment

## 5. Analytics & Reporting
✓ Risk distribution pie charts
✓ Performance trends
✓ Student rankings
✓ Department-wide analytics
✓ Semester-wise analysis

# Data Models

## User Model
```
- id (PK)
- username (unique)
- email (unique)
- password_hash
- role (student/teacher/admin)
- is_active
- created_at
```

## Student Model
```
- id (PK)
- user_id (FK)
- admission_no (unique)
- roll_no (unique)
- first_name, last_name
- dob, gender
- department, semester, section
- admission_year
- created_at
```

## AcademicRecord Model
```
- id (PK)
- student_id (FK)
- subject
- semester
- internal_marks, external_marks
- total_marks, gpa
- grade
- created_at
```

## Prediction Model
```
- id (PK)
- student_id (FK)
- semester
- predicted_gpa
- risk_level (low/medium/high)
- risk_score
- factors (JSON)
- recommendations (JSON)
- created_at
```
