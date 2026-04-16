from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import User, Student, AcademicRecord
import csv
import io
from functools import wraps

import_bp = Blueprint('import', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

@import_bp.route('/upload-csv', methods=['POST'])
@admin_required
def upload_csv():
    """Upload and import student data from CSV"""
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'message': 'File must be CSV format'}), 400
    
    try:
        # Read CSV file
        stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
        csv_data = csv.DictReader(stream)
        
        imported_count = 0
        errors = []
        
        for row_idx, row in enumerate(csv_data, 1):
            try:
                # Extract student info
                exam_score = float(row.get('Exam_Score', 0))
                previous_scores = float(row.get('Previous_Scores', 0))
                hours_studied = float(row.get('Hours_Studied', 0))
                attendance = float(row.get('Attendance', 0))
                sleep_hours = float(row.get('Sleep_Hours', 0))
                tutoring_sessions = int(row.get('Tutoring_Sessions', 0))
                physical_activity = float(row.get('Physical_Activity', 0))
                
                # Create unique identifiers
                admission_no = f"ADM{row_idx:06d}"
                roll_no = f"ROLL{row_idx:05d}"
                username = f"student_{row_idx}"
                email = f"student{row_idx}@excel.edu"
                
                # Create user account
                user = User(
                    username=username,
                    email=email,
                    role='student',
                    is_active=True
                )
                user.set_password('password123')
                db.session.add(user)
                db.session.flush()
                
                # Create student record
                student = Student(
                    user_id=user.id,
                    admission_no=admission_no,
                    roll_no=roll_no,
                    first_name=f"Student{row_idx}",
                    last_name=f"User",
                    department='Performance Analytics',
                    semester=1,
                    section='A',
                    admission_year=2025
                )
                db.session.add(student)
                db.session.flush()
                
                # Create academic records - using exam score as GPA (normalized)
                gpa = (exam_score / 100) * 4
                grade = 'A+' if exam_score >= 90 else 'A' if exam_score >= 80 else 'B' if exam_score >= 70 else 'C' if exam_score >= 60 else 'F'
                
                academic_record = AcademicRecord(
                    student_id=student.id,
                    subject='Performance Analytics',
                    semester=1,
                    internal_marks=previous_scores,
                    external_marks=exam_score,
                    total_marks=(previous_scores + exam_score) / 2,
                    gpa=gpa,
                    grade=grade
                )
                db.session.add(academic_record)
                
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_idx}: {str(e)}")
                continue
        
        db.session.commit()
        
        result = {
            'message': f'Successfully imported {imported_count} students',
            'imported_count': imported_count,
            'total_rows': row_idx
        }
        
        if errors:
            result['errors'] = errors
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error processing file: {str(e)}'}), 400

@import_bp.route('/manual-entry', methods=['POST'])
@admin_required
def manual_student_entry():
    """Manually add a single student"""
    
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'admission_no', 'exam_score', 'previous_scores']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    try:
        # Create user account
        username = data.get('username') or f"student_{data['admission_no']}"
        email = data.get('email') or f"{data['first_name'].lower()}@excel.edu"
        
        user = User(
            username=username,
            email=email,
            role='student',
            is_active=True
        )
        user.set_password(data.get('password', 'password123'))
        db.session.add(user)
        db.session.flush()
        
        # Create student record
        student = Student(
            user_id=user.id,
            admission_no=data['admission_no'],
            roll_no=data.get('roll_no', f"ROLL{user.id:05d}"),
            first_name=data['first_name'],
            last_name=data['last_name'],
            department=data.get('department', 'Information Technology'),
            semester=int(data.get('semester', 1)),
            section=data.get('section', 'A'),
            admission_year=int(data.get('admission_year', 2025))
        )
        db.session.add(student)
        db.session.flush()
        
        # Create academic record
        exam_score = float(data['exam_score'])
        previous_scores = float(data['previous_scores'])
        gpa = (exam_score / 100) * 4
        grade = 'A+' if exam_score >= 90 else 'A' if exam_score >= 80 else 'B' if exam_score >= 70 else 'C' if exam_score >= 60 else 'F'
        
        academic_record = AcademicRecord(
            student_id=student.id,
            subject=data.get('subject', 'Performance Analytics'),
            semester=int(data.get('semester', 1)),
            internal_marks=previous_scores,
            external_marks=exam_score,
            total_marks=(previous_scores + exam_score) / 2,
            gpa=gpa,
            grade=grade
        )
        db.session.add(academic_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Student registered successfully',
            'student_id': student.id,
            'user_id': user.id,
            'username': username,
            'email': email
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating student: {str(e)}'}), 400
