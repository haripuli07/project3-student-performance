from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import User, Student, Administrator, Prediction, AcademicRecord
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    total_students = Student.query.count()
    total_predictions = Prediction.query.count()
    
    high_risk_students = Prediction.query.filter_by(risk_level='high').count()
    medium_risk_students = Prediction.query.filter_by(risk_level='medium').count()
    low_risk_students = Prediction.query.filter_by(risk_level='low').count()
    
    avg_gpa = db.session.query(db.func.avg(AcademicRecord.gpa)).scalar() or 0
    
    return jsonify({
        'total_students': total_students,
        'total_predictions': total_predictions,
        'risk_distribution': {
            'high': high_risk_students,
            'medium': medium_risk_students,
            'low': low_risk_students
        },
        'average_gpa': round(avg_gpa, 2)
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    role = request.args.get('role')
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    
    users = query.all()
    users_list = []
    
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
        users_list.append(user_data)
    
    return jsonify(users_list), 200

@admin_bp.route('/users/<int:user_id>/toggle', methods=['PUT'])
@admin_required
def toggle_user_status(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({'message': 'User status updated', 'is_active': user.is_active}), 200

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['student', 'teacher', 'admin']:
        return jsonify({'message': 'Invalid role'}), 400
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({'message': 'User role updated', 'role': user.role}), 200

@admin_bp.route('/analytics/risk-distribution', methods=['GET'])
@admin_required
def get_risk_distribution():
    semester = request.args.get('semester', type=int)
    
    query = Prediction.query
    if semester:
        query = query.filter_by(semester=semester)
    
    predictions = query.all()
    
    distribution = {
        'high': len([p for p in predictions if p.risk_level == 'high']),
        'medium': len([p for p in predictions if p.risk_level == 'medium']),
        'low': len([p for p in predictions if p.risk_level == 'low'])
    }
    
    return jsonify(distribution), 200

@admin_bp.route('/analytics/top-performers', methods=['GET'])
@admin_required
def get_top_performers():
    limit = request.args.get('limit', 10, type=int)
    
    top_students = db.session.query(
        Student.id,
        Student.first_name,
        Student.last_name,
        Student.admission_no,
        db.func.avg(AcademicRecord.gpa).label('avg_gpa')
    ).join(AcademicRecord).group_by(Student.id).order_by(db.desc('avg_gpa')).limit(limit).all()
    
    performers = []
    for student in top_students:
        performers.append({
            'student_id': student[0],
            'name': f"{student[1]} {student[2]}",
            'admission_no': student[3],
            'average_gpa': round(student[4], 2) if student[4] else 0
        })
    
    return jsonify(performers), 200

@admin_bp.route('/analytics/at-risk-students', methods=['GET'])
@admin_required
def get_at_risk_students():
    limit = request.args.get('limit', 10, type=int)
    
    at_risk = Prediction.query.filter_by(risk_level='high').order_by(
        Prediction.risk_score.desc()
    ).limit(limit).all()
    
    students_list = []
    for pred in at_risk:
        student = Student.query.get(pred.student_id)
        students_list.append({
            'student_id': student.id,
            'name': f"{student.first_name} {student.last_name}",
            'admission_no': student.admission_no,
            'risk_score': round(pred.risk_score, 2),
            'factors': pred.factors,
            'recommendations': pred.recommendations
        })
    
    return jsonify(students_list), 200
