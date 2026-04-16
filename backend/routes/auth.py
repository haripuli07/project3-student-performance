from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User, Student, Administrator
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'student')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    if data.get('role') == 'student':
        student = Student(
            user_id=user.id,
            admission_no=data.get('admission_no'),
            roll_no=data.get('roll_no'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            department=data.get('department'),
            semester=data.get('semester', 1)
        )
        db.session.add(student)
        db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'User account is inactive'}), 403
    
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=30))
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user_id': user.id,
        'role': user.role,
        'username': user.username
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }
    
    if user.student:
        user_data['student'] = {
            'id': user.student.id,
            'admission_no': user.student.admission_no,
            'roll_no': user.student.roll_no,
            'first_name': user.student.first_name,
            'last_name': user.student.last_name
        }
    
    return jsonify(user_data), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    
    if not user.check_password(data.get('current_password')):
        return jsonify({'message': 'Current password is incorrect'}), 401
    
    user.set_password(data.get('new_password'))
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200
