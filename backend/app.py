from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from database import db

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Database Configuration (SQLite for development, PostgreSQL for production)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///student_performance.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

    db.init_app(app)
    jwt.init_app(app)

    # Import blueprints
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.predictions import predictions_bp
    from routes.admin import admin_bp
    from routes.import_data import import_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(import_bp, url_prefix='/api/import')
    
    return app


app = create_app()

# Create tables when the app is created (needed for gunicorn/Render)
with app.app_context():
    db.create_all()

# Add a default route for '/'
@app.route('/')
def index():
    return '<h2>Welcome to the Student Performance API. Try /api/health for a health check.</h2>'

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
