from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import User, Student, Prediction, AcademicRecord, Attendance
import sys
import os

# Add ml_model to path for predictor import
ml_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_model'))
if ml_model_path not in sys.path:
    sys.path.insert(0, ml_model_path)

from predictor import PerformancePredictor

predictions_bp = Blueprint('predictions', __name__)
predictor = PerformancePredictor()

@predictions_bp.route('/predict/<int:student_id>', methods=['GET'])
@jwt_required()
def predict_performance(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    if user.role != 'admin' and (not user.student or user.student.id != student_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    try:
        academic_data = AcademicRecord.query.filter_by(student_id=student_id).all()
        attendance_data = Attendance.query.filter_by(student_id=student_id).all()
        
        if not academic_data or not attendance_data:
            return jsonify({'message': 'Insufficient data for prediction'}), 400
        
        features = extract_features(academic_data, attendance_data)
        predicted_gpa, risk_level, risk_score, factors, recommendations = predictor.predict(features)
        
        prediction = Prediction(
            student_id=student_id,
            semester=student.semester,
            predicted_gpa=predicted_gpa,
            risk_level=risk_level,
            risk_score=risk_score,
            factors=factors,
            recommendations=recommendations
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'student_id': student_id,
            'predicted_gpa': predicted_gpa,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'factors': factors,
            'recommendations': recommendations,
            'prediction_id': prediction.id
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Prediction failed: {str(e)}'}), 500

@predictions_bp.route('/history/<int:student_id>', methods=['GET'])
@jwt_required()
def get_prediction_history(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    student = Student.query.get(student_id)
    
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    if user.role != 'admin' and (not user.student or user.student.id != student_id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    predictions = Prediction.query.filter_by(student_id=student_id).order_by(Prediction.created_at.desc()).all()
    
    prediction_list = []
    for pred in predictions:
        prediction_list.append({
            'id': pred.id,
            'predicted_gpa': pred.predicted_gpa,
            'risk_level': pred.risk_level,
            'risk_score': pred.risk_score,
            'created_at': pred.created_at.isoformat(),
            'factors': pred.factors,
            'recommendations': pred.recommendations
        })
    
    return jsonify(prediction_list), 200

@predictions_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_predictions():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    semester = request.args.get('semester', type=int)
    risk_level = request.args.get('risk_level')
    
    query = Prediction.query
    
    if semester:
        query = query.filter_by(semester=semester)
    if risk_level:
        query = query.filter_by(risk_level=risk_level)
    
    predictions = query.all()
    
    prediction_list = []
    for pred in predictions:
        student = Student.query.get(pred.student_id)
        prediction_list.append({
            'id': pred.id,
            'student_id': pred.student_id,
            'student_name': f"{student.first_name} {student.last_name}",
            'admission_no': student.admission_no,
            'predicted_gpa': pred.predicted_gpa,
            'risk_level': pred.risk_level,
            'risk_score': pred.risk_score,
            'created_at': pred.created_at.isoformat()
        })
    
    return jsonify(prediction_list), 200

def extract_features(academic_data, attendance_data):
    """Extract features from academic and attendance data for ML model"""
    avg_gpa = sum([record.gpa for record in academic_data if record.gpa]) / max(len(academic_data), 1)
    avg_attendance = sum([att.attendance_percentage for att in attendance_data]) / max(len(attendance_data), 1)
    total_subjects = len(academic_data)
    avg_internal = sum([record.internal_marks for record in academic_data if record.internal_marks]) / max(len(academic_data), 1)
    avg_external = sum([record.external_marks for record in academic_data if record.external_marks]) / max(len(academic_data), 1)
    
    return {
        'avg_gpa': avg_gpa or 0,
        'avg_attendance': avg_attendance or 0,
        'total_subjects': total_subjects,
        'avg_internal_marks': avg_internal or 0,
        'avg_external_marks': avg_external or 0
    }
