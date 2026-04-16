-- Initial database schema

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    admission_no VARCHAR(50) UNIQUE NOT NULL,
    roll_no VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    dob DATE,
    gender VARCHAR(10),
    department VARCHAR(100),
    semester INTEGER,
    section VARCHAR(10),
    admission_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create academic records table
CREATE TABLE academic_records (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    semester INTEGER,
    internal_marks FLOAT,
    external_marks FLOAT,
    total_marks FLOAT,
    gpa FLOAT,
    grade VARCHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Create attendance table
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    semester INTEGER,
    classes_attended INTEGER DEFAULT 0,
    total_classes INTEGER DEFAULT 0,
    attendance_percentage FLOAT DEFAULT 0.0,
    month VARCHAR(20),
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Create predictions table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    semester INTEGER,
    predicted_gpa FLOAT,
    risk_level VARCHAR(20),
    risk_score FLOAT,
    factors JSONB,
    recommendations JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Create administrators table
CREATE TABLE administrators (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    full_name VARCHAR(120),
    role_type VARCHAR(50),
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_academic_records_student_id ON academic_records(student_id);
CREATE INDEX idx_attendance_student_id ON attendance(student_id);
CREATE INDEX idx_predictions_student_id ON predictions(student_id);
CREATE INDEX idx_predictions_risk_level ON predictions(risk_level);
