# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All endpoints (except login/register) require JWT token in header:
```
Authorization: Bearer <token>
```

## Response Format
```json
{
  "data": {},
  "message": "Success message",
  "status": 200
}
```

## Error Handling
```json
{
  "message": "Error message",
  "status": 400
}
```

## Endpoints

### Authentication

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "username": "student123",
  "email": "student@excel.edu",
  "password": "password123",
  "role": "student",
  "admission_no": "22EGIT111",
  "roll_no": "2IT069",
  "first_name": "John",
  "last_name": "Doe",
  "department": "IT",
  "semester": 8
}
```

**Response (201)**
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "username": "student123",
  "password": "password123"
}
```

**Response (200)**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1,
  "role": "student",
  "username": "student123"
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "id": 1,
  "username": "student123",
  "email": "student@excel.edu",
  "role": "student",
  "student": {
    "id": 1,
    "admission_no": "22EGIT111",
    "roll_no": "2IT069",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### Change Password
```
POST /auth/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

### Students

#### Get All Students (Admin Only)
```
GET /students
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "admission_no": "22EGIT111",
    "roll_no": "2IT069",
    "name": "John Doe",
    "department": "Information Technology",
    "semester": 8,
    "section": "C"
  }
]
```

#### Get Student Details
```
GET /students/:student_id
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "id": 1,
  "admission_no": "22EGIT111",
  "roll_no": "2IT069",
  "first_name": "John",
  "last_name": "Doe",
  "department": "Information Technology",
  "semester": 8,
  "section": "C",
  "academic_records": [
    {
      "id": 1,
      "subject": "Data Structures",
      "semester": 8,
      "internal_marks": 35,
      "external_marks": 72,
      "total_marks": 107,
      "gpa": 3.6,
      "grade": "A"
    }
  ],
  "attendance": [
    {
      "id": 1,
      "subject": "Data Structures",
      "semester": 8,
      "attendance_percentage": 92.5,
      "month": "April"
    }
  ]
}
```

#### Add Academic Record
```
POST /students/:student_id/academic
Authorization: Bearer <token>
Content-Type: application/json

{
  "subject": "Data Structures",
  "semester": 8,
  "internal_marks": 35,
  "external_marks": 72,
  "total_marks": 107,
  "gpa": 3.6,
  "grade": "A"
}
```

#### Add Attendance Record
```
POST /students/:student_id/attendance
Authorization: Bearer <token>
Content-Type: application/json

{
  "subject": "Data Structures",
  "semester": 8,
  "classes_attended": 42,
  "total_classes": 45,
  "attendance_percentage": 93.33,
  "month": "April",
  "year": 2026
}
```

### Predictions

#### Generate Prediction
```
GET /predictions/predict/:student_id
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "student_id": 1,
  "predicted_gpa": 3.7,
  "risk_level": "low",
  "risk_score": 0.15,
  "factors": {
    "attendance": {
      "value": 92.5,
      "status": "good",
      "weight": "low"
    },
    "academic_performance": {
      "current_gpa": 3.6,
      "predicted_gpa": 3.7,
      "trend": "improving",
      "change": 0.1
    },
    "assessment_balance": {
      "internal_marks": 35,
      "external_marks": 72,
      "imbalance": "balanced"
    }
  },
  "recommendations": [
    "Continue current study habits",
    "Consider helping peers as part of learning"
  ],
  "prediction_id": 1
}
```

#### Get Prediction History
```
GET /predictions/history/:student_id
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "predicted_gpa": 3.7,
    "risk_level": "low",
    "risk_score": 0.15,
    "created_at": "2026-04-16T10:30:00",
    "factors": {},
    "recommendations": []
  }
]
```

#### Get All Predictions (Admin Only)
```
GET /predictions/all?semester=8&risk_level=high
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "student_id": 2,
    "student_name": "Jane Smith",
    "admission_no": "22EGIT112",
    "predicted_gpa": 2.1,
    "risk_level": "high",
    "risk_score": 0.85,
    "created_at": "2026-04-16T10:30:00"
  }
]
```

### Admin

#### Dashboard
```
GET /admin/dashboard
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "total_students": 5,
  "total_predictions": 12,
  "risk_distribution": {
    "high": 2,
    "medium": 1,
    "low": 2
  },
  "average_gpa": 3.42
}
```

#### Get All Users
```
GET /admin/users?role=student
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "id": 1,
    "username": "student123",
    "email": "student@excel.edu",
    "role": "student",
    "is_active": true,
    "created_at": "2026-04-16T10:30:00"
  }
]
```

#### Toggle User Status
```
PUT /admin/users/:user_id/toggle
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "message": "User status updated",
  "is_active": false
}
```

#### Update User Role
```
PUT /admin/users/:user_id/role
Authorization: Bearer <token>
Content-Type: application/json

{
  "role": "teacher"
}
```

#### Risk Distribution
```
GET /admin/analytics/risk-distribution?semester=8
Authorization: Bearer <token>
```

**Response (200)**
```json
{
  "high": 2,
  "medium": 1,
  "low": 2
}
```

#### Top Performers
```
GET /admin/analytics/top-performers?limit=10
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "student_id": 1,
    "name": "John Doe",
    "admission_no": "22EGIT111",
    "average_gpa": 3.8
  }
]
```

#### At-Risk Students
```
GET /admin/analytics/at-risk-students?limit=10
Authorization: Bearer <token>
```

**Response (200)**
```json
[
  {
    "student_id": 2,
    "name": "Jane Smith",
    "admission_no": "22EGIT112",
    "risk_score": 0.85,
    "factors": {},
    "recommendations": []
  }
]
```

## Status Codes

- **200**: OK - Request successful
- **201**: Created - Resource created successfully
- **400**: Bad Request - Invalid request parameters
- **401**: Unauthorized - Missing or invalid authentication
- **403**: Forbidden - Access denied (insufficient permissions)
- **404**: Not Found - Resource not found
- **500**: Internal Server Error - Server error

## Rate Limiting

Currently not implemented. Can be added using Flask-Limiter for production.

## Pagination

Future implementation for list endpoints:
```
GET /endpoint?page=1&limit=20
```

## Searching & Filtering

Implemented for admin endpoints:
- `?role=admin` - Filter by role
- `?semester=8` - Filter by semester
- `?risk_level=high` - Filter by risk level
