from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, admin, teacher
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    admission_no = db.Column(db.String(50), unique=True, nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    department = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    section = db.Column(db.String(10))
    admission_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    academic_records = db.relationship('AcademicRecord', backref='student', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='student', cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='student', cascade='all, delete-orphan')

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer)
    internal_marks = db.Column(db.Float)
    external_marks = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    gpa = db.Column(db.Float)
    grade = db.Column(db.String(2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer)
    classes_attended = db.Column(db.Integer, default=0)
    total_classes = db.Column(db.Integer, default=0)
    attendance_percentage = db.Column(db.Float, default=0.0)
    month = db.Column(db.String(20))
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    semester = db.Column(db.Integer)
    predicted_gpa = db.Column(db.Float)
    risk_level = db.Column(db.String(20))  # low, medium, high
    risk_score = db.Column(db.Float)
    factors = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Administrator(db.Model):
    __tablename__ = 'administrators'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(120))
    role_type = db.Column(db.String(50))  # superadmin, admin, moderator
    permissions = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
