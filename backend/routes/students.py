from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import User, Student, AcademicRecord, Attendance

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    students = Student.query.all()
    students_list = []
    
    for student in students:
        students_list.append({
            'id': student.id,
            'admission_no': student.admission_no,
            'roll_no': student.roll_no,
            'name': f"{student.first_name} {student.last_name}",
            'department': student.department,
            'semester': student.semester,
            'section': student.section
        })
    
    return jsonify(students_list), 200

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    if user.role != 'admin' and (not user.student or user.student.id != student_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    academic_records = [{
        'id': record.id,
        'subject': record.subject,
        'semester': record.semester,
        'internal_marks': record.internal_marks,
        'external_marks': record.external_marks,
        'total_marks': record.total_marks,
        'gpa': record.gpa,
        'grade': record.grade
    } for record in student.academic_records]
    
    attendance = [{
        'id': att.id,
        'subject': att.subject,
        'semester': att.semester,
        'attendance_percentage': att.attendance_percentage,
        'month': att.month
    } for att in student.attendance_records]
    
    return jsonify({
        'id': student.id,
        'admission_no': student.admission_no,
        'roll_no': student.roll_no,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'department': student.department,
        'semester': student.semester,
        'section': student.section,
        'academic_records': academic_records,
        'attendance': attendance
    }), 200

@students_bp.route('/<int:student_id>/academic', methods=['POST'])
@jwt_required()
def add_academic_record(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'admin' and user.role != 'teacher':
        return jsonify({'message': 'Unauthorized'}), 403
    
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    data = request.get_json()
    
    record = AcademicRecord(
        student_id=student_id,
        subject=data.get('subject'),
        semester=data.get('semester'),
        internal_marks=data.get('internal_marks'),
        external_marks=data.get('external_marks'),
        total_marks=data.get('total_marks'),
        gpa=data.get('gpa'),
        grade=data.get('grade')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({'message': 'Academic record added', 'record_id': record.id}), 201

@students_bp.route('/<int:student_id>/attendance', methods=['POST'])
@jwt_required()
def add_attendance(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'admin' and user.role != 'teacher':
        return jsonify({'message': 'Unauthorized'}), 403
    
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    data = request.get_json()
    
    attendance = Attendance(
        student_id=student_id,
        subject=data.get('subject'),
        semester=data.get('semester'),
        classes_attended=data.get('classes_attended'),
        total_classes=data.get('total_classes'),
        attendance_percentage=data.get('classes_attended', 0) / max(data.get('total_classes', 1), 1) * 100,
        month=data.get('month'),
        year=data.get('year')
    )
    
    db.session.add(attendance)
    db.session.commit()
    
    return jsonify({'message': 'Attendance record added', 'record_id': attendance.id}), 201
