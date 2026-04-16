import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

class PerformancePredictor:
    def __init__(self):
        self.model_dir = os.path.dirname(__file__)
        self.regressor_path = os.path.join(self.model_dir, 'models', 'gpa_predictor.pkl')
        self.classifier_path = os.path.join(self.model_dir, 'models', 'risk_classifier.pkl')
        self.scaler_path = os.path.join(self.model_dir, 'models', 'scaler.pkl')
        
        # Ensure model directory exists
        os.makedirs(os.path.join(self.model_dir, 'models'), exist_ok=True)
        
        # Load or initialize models
        self.load_or_initialize_models()
    
    def load_or_initialize_models(self):
        """Load existing models or initialize new ones"""
        if os.path.exists(self.regressor_path):
            self.gpa_regressor = joblib.load(self.regressor_path)
            self.risk_classifier = joblib.load(self.classifier_path)
            self.scaler = joblib.load(self.scaler_path)
        else:
            # Initialize models with dummy training
            self.initialize_models()
    
    def initialize_models(self):
        """Initialize models with dummy training data"""
        # Create dummy training data
        X_dummy = np.array([
            [3.5, 85, 5, 80, 75],
            [2.8, 75, 6, 70, 65],
            [3.2, 80, 5, 75, 70],
            [2.0, 60, 4, 50, 55],
            [3.8, 90, 6, 85, 80],
        ])
        
        y_gpa = np.array([3.6, 2.9, 3.3, 2.1, 3.9])
        y_risk = np.array([0, 1, 0, 2, 0])  # 0=low, 1=medium, 2=high
        
        # Initialize and train scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_dummy)
        
        # Initialize and train models
        self.gpa_regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.gpa_regressor.fit(X_scaled, y_gpa)
        
        self.risk_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_classifier.fit(X_scaled, y_risk)
        
        # Save models
        os.makedirs(os.path.join(self.model_dir, 'models'), exist_ok=True)
        joblib.dump(self.gpa_regressor, self.regressor_path)
        joblib.dump(self.risk_classifier, self.classifier_path)
        joblib.dump(self.scaler, self.scaler_path)
    
    def predict(self, features):
        """
        Predict student performance
        features: dict with keys: avg_gpa, avg_attendance, total_subjects, avg_internal_marks, avg_external_marks
        """
        try:
            # Extract features
            feature_vector = np.array([[
                features.get('avg_gpa', 0),
                features.get('avg_attendance', 0),
                features.get('total_subjects', 0),
                features.get('avg_internal_marks', 0),
                features.get('avg_external_marks', 0)
            ]])
            
            # Scale features
            X_scaled = self.scaler.transform(feature_vector)
            
            # Make predictions
            predicted_gpa = float(self.gpa_regressor.predict(X_scaled)[0])
            risk_class = int(self.risk_classifier.predict(X_scaled)[0])
            risk_probabilities = self.risk_classifier.predict_proba(X_scaled)[0]
            
            # Map risk class to label
            risk_levels = ['low', 'medium', 'high']
            risk_level = risk_levels[risk_class]
            risk_score = float(risk_probabilities[risk_class])
            
            # Generate factors and recommendations
            factors = self.generate_factors(features, predicted_gpa, risk_level)
            recommendations = self.generate_recommendations(risk_level, factors)
            
            return predicted_gpa, risk_level, risk_score, factors, recommendations
        
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            raise
    
    def generate_factors(self, features, predicted_gpa, risk_level):
        """Generate factors affecting student performance"""
        factors = {}
        
        # Attendance factor
        attendance = features.get('avg_attendance', 0)
        if attendance < 75:
            factors['attendance'] = {
                'value': round(attendance, 2),
                'status': 'critical',
                'weight': 'high'
            }
        elif attendance < 85:
            factors['attendance'] = {
                'value': round(attendance, 2),
                'status': 'warning',
                'weight': 'medium'
            }
        else:
            factors['attendance'] = {
                'value': round(attendance, 2),
                'status': 'good',
                'weight': 'low'
            }
        
        # Academic performance factor
        current_gpa = features.get('avg_gpa', 0)
        gpa_trend = predicted_gpa - current_gpa
        factors['academic_performance'] = {
            'current_gpa': round(current_gpa, 2),
            'predicted_gpa': round(predicted_gpa, 2),
            'trend': 'improving' if gpa_trend > 0 else 'declining' if gpa_trend < 0 else 'stable',
            'change': round(gpa_trend, 2)
        }
        
        # Internal vs External marks
        internal = features.get('avg_internal_marks', 0)
        external = features.get('avg_external_marks', 0)
        factors['assessment_balance'] = {
            'internal_marks': round(internal, 2),
            'external_marks': round(external, 2),
            'imbalance': 'high' if abs(internal - external) > 15 else 'moderate' if abs(internal - external) > 5 else 'balanced'
        }
        
        return factors
    
    def generate_recommendations(self, risk_level, factors):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append('Request immediate intervention with academic advisor')
            recommendations.append('Join peer tutoring sessions')
            recommendations.append('Create a personalized study plan')
            
            if factors['attendance']['value'] < 75:
                recommendations.append('Improve attendance - it is critical for success')
            
            if factors['assessment_balance']['imbalance'] == 'high':
                recommendations.append('Focus on improving external exam performance')
        
        elif risk_level == 'medium':
            recommendations.append('Schedule regular check-ins with mentor')
            recommendations.append('Review study techniques for challenging subjects')
            recommendations.append('Maintain consistent attendance')
            
            if factors['attendance']['value'] < 80:
                recommendations.append('Increase attendance to at least 80%')
        
        else:  # low risk
            recommendations.append('Continue current study habits')
            recommendations.append('Consider helping peers as part of learning')
            recommendations.append('Explore advanced topics in your field')
        
        return recommendations
    
    def train_with_new_data(self, X_train, y_gpa_train, y_risk_train):
        """Train models with new student data"""
        try:
            # Scale new data
            X_scaled = self.scaler.fit_transform(X_train)
            
            # Retrain models
            self.gpa_regressor.fit(X_scaled, y_gpa_train)
            self.risk_classifier.fit(X_scaled, y_risk_train)
            
            # Save updated models
            joblib.dump(self.gpa_regressor, self.regressor_path)
            joblib.dump(self.risk_classifier, self.classifier_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            return True
        except Exception as e:
            print(f"Training error: {str(e)}")
            return False
