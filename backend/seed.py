# Seed data script for testing

from app import app, db
from models import User, Student, AcademicRecord, Attendance, Administrator
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        # Create all tables first
        db.create_all()
        
        # Clear existing data (safely - only delete if tables exist)
        db.session.query(Attendance).delete()
        db.session.query(AcademicRecord).delete()
        db.session.query(Student).delete()
        db.session.query(Administrator).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@excel.edu',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        
        admin = Administrator(
            user_id=admin_user.id,
            full_name='System Administrator',
            role_type='superadmin',
            permissions={'all': True}
        )
        db.session.add(admin)
        
        # Create test students
        student_data = [
            {'admission_no': '22EGIT111', 'roll_no': '2IT069', 'first_name': 'Hariprasath', 'last_name': 'M'},
            {'admission_no': '22EGIT112', 'roll_no': '2IT070', 'first_name': 'Arjun', 'last_name': 'Kumar'},
            {'admission_no': '22EGIT113', 'roll_no': '2IT071', 'first_name': 'Priya', 'last_name': 'Singh'},
            {'admission_no': '22EGIT114', 'roll_no': '2IT072', 'first_name': 'Rahul', 'last_name': 'Sharma'},
            {'admission_no': '22EGIT115', 'roll_no': '2IT073', 'first_name': 'Neha', 'last_name': 'Patel'},
        ]
        
        subjects = ['DataStructures', 'WebDevelopment', 'DATABASE', 'MachineLearning', 'CloudComputing']
        
        for std in student_data:
            # Create user
            user = User(
                username=std['admission_no'].lower(),
                email=f"{std['first_name'].lower()}@excel.edu",
                role='student',
                is_active=True
            )
            user.set_password('student123')
            db.session.add(user)
            db.session.commit()
            
            # Create student
            student = Student(
                user_id=user.id,
                admission_no=std['admission_no'],
                roll_no=std['roll_no'],
                first_name=std['first_name'],
                last_name=std['last_name'],
                department='Information Technology',
                semester=8,
                section='C',
                admission_year=2022
            )
            db.session.add(student)
            db.session.commit()
            
            # Add academic records
            for subject in subjects:
                internal = random.uniform(20, 40)
                external = random.uniform(40, 80)
                total = internal + external
                
                gpa = total / 100 * 4
                
                if total >= 90:
                    grade = 'A+'
                elif total >= 80:
                    grade = 'A'
                elif total >= 70:
                    grade = 'B'
                elif total >= 60:
                    grade = 'C'
                else:
                    grade = 'F'
                
                record = AcademicRecord(
                    student_id=student.id,
                    subject=subject,
                    semester=8,
                    internal_marks=internal,
                    external_marks=external,
                    total_marks=total,
                    gpa=gpa,
                    grade=grade
                )
                db.session.add(record)
            
            # Add attendance records
            for subject in subjects:
                classes_attended = random.randint(35, 45)
                total_classes = 45
                attendance_pct = (classes_attended / total_classes) * 100
                
                attendance = Attendance(
                    student_id=student.id,
                    subject=subject,
                    semester=8,
                    classes_attended=classes_attended,
                    total_classes=total_classes,
                    attendance_percentage=attendance_pct,
                    month='April',
                    year=2026
                )
                db.session.add(attendance)
            
            db.session.commit()
        
        print("✓ Database seeded successfully!")
        print("Admin user: admin / admin123")
        print("Student users: 22egit111-115 / student123")

if __name__ == '__main__':
    seed_database()
