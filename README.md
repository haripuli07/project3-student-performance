# Student Performance Predictor - Fullstack Application

A comprehensive web application for predicting student academic performance using Machine Learning with admin controls and a user-friendly interface.

## Features

- **Machine Learning Analysis**: Uses scikit-learn models (RandomForest, GradientBoosting) to predict student performance
- **Risk Assessment**: Identifies high-risk, medium-risk, and low-risk students
- **Admin Dashboard**: Comprehensive analytics and student management
- **Student Dashboard**: Personalized performance analysis and recommendations
- **JWT Authentication**: Secure login and role-based access control
- **Database**: PostgreSQL for reliable data storage
- **Responsive UI**: Built with React and Tailwind CSS

## Architecture

```
├── backend/                    # Flask REST API
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── students.py        # Student data management
│   │   ├── predictions.py     # ML predictions
│   │   └── admin.py           # Admin analytics
│   ├── models.py              # SQLAlchemy database models
│   ├── app.py                 # Flask application
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React application
│   ├── src/
│   │   ├── pages/             # Page components
│   │   ├── components/        # Reusable components
│   │   ├── store/             # Zustand state management
│   │   └── App.js             # Main app component
│   └── package.json           # Node dependencies
├── ml_model/                  # Machine Learning module
│   ├── predictor.py          # ML prediction engine
│   └── models/               # Trained models storage
├── database/                 # Database configuration
│   └── init.sql             # Database schema
└── docker-compose.yml        # Docker configuration
```

## Tech Stack

**Backend:**
- Flask 2.3.0
- SQLAlchemy ORM
- scikit-learn (ML)
- PostgreSQL
- Flask-JWT-Extended (Auth)

**Frontend:**
- React 18.2.0
- React Router
- Axios
- Tailwind CSS
- Zustand (State Management)
- Chart.js (Visualizations)

**Database:**
- PostgreSQL 15
- JSONB for flexible data storage

**DevOps:**
- Docker & Docker Compose
- Python 3.11
- Node.js 18

## Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+
- Node.js 18+
- PostgreSQL 15 (if not using Docker)

### Method 1: Using Docker (Recommended)

```bash
# Clone the repository
cd project3

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### Method 2: Local Development

**Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python -c "from app import db; db.create_all()"

# Run Flask server
python app.py
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start React development server
npm start
```

## Database Setup

### Option 1: Automatic (Docker)
The database is automatically initialized when using Docker Compose.

### Option 2: Manual PostgreSQL

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE student_performance;

# Run schema
\c student_performance
\i database/init.sql
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/change-password` - Change password

### Students
- `GET /api/students` - List all students (admin only)
- `GET /api/students/<id>` - Get student details
- `POST /api/students/<id>/academic` - Add academic record
- `POST /api/students/<id>/attendance` - Add attendance record

### Predictions
- `GET /api/predictions/predict/<id>` - Generate prediction
- `GET /api/predictions/history/<id>` - Prediction history
- `GET /api/predictions/all` - All predictions (admin)

### Admin
- `GET /api/admin/dashboard` - Dashboard metrics
- `GET /api/admin/users` - All users
- `PUT /api/admin/users/<id>/role` - Update user role
- `GET /api/admin/analytics/risk-distribution` - Risk analytics
- `GET /api/admin/analytics/top-performers` - Top students
- `GET /api/admin/analytics/at-risk-students` - At-risk students

## Machine Learning Model

### Features Used
- Average GPA
- Attendance percentage
- Number of subjects
- Average internal marks
- Average external marks

### Models
- **GPA Predictor**: Gradient Boosting Regressor for continuous GPA prediction
- **Risk Classifier**: Random Forest for risk level classification

### Risk Levels
- **Low Risk**: Student performing well
- **Medium Risk**: Student needs attention
- **High Risk**: Student requires immediate intervention

## Admin Dashboard Features

- **Dashboard Metrics**: Total students, predictions, risk distribution, average GPA
- **Risk Distribution Chart**: Visual representation of student risk levels
- **Top Performers**: List of students with highest GPAs
- **At-Risk Students**: Students needing immediate intervention
- **User Management**: Enable/disable users, change roles
- **Analytics**: In-depth performance analytics

## Student Dashboard Features

- **Performance Analysis**: Current and predicted GPA
- **Risk Assessment**: Individual risk level and score
- **Performance Factors**: Attendance, academic trends, assessment balance
- **Recommendations**: Personalized improvement suggestions
- **Academic Records**: Complete grade history
- **Prediction History**: Track performance predictions over time

## Default Credentials

```
Username: admin
Password: admin123
Role: admin
```

## Key Features

### For Students
✓ View personal performance analysis
✓ Get personalized recommendations
✓ Track academic progress
✓ Understand risk factors affecting performance
✓ Generate performance predictions

### For Admins
✓ Comprehensive dashboard with key metrics
✓ Risk distribution analytics
✓ Identify top performers
✓ Monitor at-risk students
✓ User management and role assignment
✓ Generate reports and insights

## ML Model Accuracy

The model is trained on:
- Student attendance records
- Academic performance history
- GPA trends
- Internal vs external assessment balance

Initial training data provides baseline accuracy. Model improves as more student data is added to the system.

## File Structure

```
project3/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── students.py
│       ├── predictions.py
│       └── admin.py
├── frontend/
│   ├── package.json
│   ├── Dockerfile
│   ├── .env.example
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── components/
│       ├── pages/
│       ├── store/
│       └── utils/
├── ml_model/
│   ├── predictor.py
│   ├── requirements.txt
│   └── models/
├── database/
│   └── init.sql
├── docker-compose.yml
└── README.md
```

## Performance & Scalability

- **Database**: Indexed queries for fast retrieval
- **API**: RESTful architecture with JWT auth
- **ML**: Efficient scikit-learn models
- **Frontend**: React with component memoization
- **Caching**: Can be enhanced with Redis

## Security Measures

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)

## Future Enhancements

- [ ] Email notifications for at-risk students
- [ ] Advanced analytics with more ML models
- [ ] Student progress tracking over semesters
- [ ] Peer comparison analytics
- [ ] Export reports (PDF/Excel)
- [ ] Mobile app
- [ ] Real-time notifications
- [ ] Multi-language support

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart services
docker-compose restart
```

### Frontend Not Loading API
- Check if backend is running: `http://localhost:5000/api/health`
- Verify REACT_APP_API_URL in `.env`
- Check browser console for errors

### Model Training Issues
- Ensure sufficient data points
- Check feature ranges and normalization
- Validate input data format

## Support & Documentation

For more information, check individual component files for docstrings and comments.

## License

This project is for educational purposes. Modify and distribute as needed.

## Contributors

Created for Excel Engineering College
