#!/usr/bin/env python3
"""
Test script for CSV import and manual entry endpoints
"""
import requests
import json
import csv
import os

# Configuration
BACKEND_URL = "http://localhost:5000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def get_admin_token():
    """Login as admin to get JWT token"""
    print("\n[1/5] Getting admin token...")
    response = requests.post(
        f"{BACKEND_URL}/api/auth/login",
        json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return None
    
    data = response.json()
    token = data.get("access_token")
    print(f"✅ Got token: {token[:20]}...")
    return token

def test_manual_entry(token):
    """Test manual student entry endpoint"""
    print("\n[2/5] Testing manual student entry...")
    headers = {"Authorization": f"Bearer {token}"}
    
    student_data = {
        "first_name": "Test",
        "last_name": "Student",
        "admission_no": "TEST001",
        "exam_score": 85,
        "previous_scores": 80,
        "email": "test@excel.edu",
        "department": "Information Technology",
        "semester": 1
    }
    
    response = requests.post(
        f"{BACKEND_URL}/api/import/manual-entry",
        json=student_data,
        headers=headers
    )
    
    if response.status_code != 201:
        print(f"❌ Manual entry failed: {response.text}")
        return False
    
    data = response.json()
    print(f"✅ Manual entry successful!")
    print(f"   Student ID: {data['student_id']}, Username: {data['username']}")
    return True

def test_csv_upload(token):
    """Test CSV upload endpoint"""
    print("\n[3/5] Testing CSV upload...")
    
    csv_path = os.path.join(os.path.dirname(__file__), "StudentPerformanceFactors.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at {csv_path}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{BACKEND_URL}/api/import/upload-csv",
                files=files,
                headers=headers
            )
        
        if response.status_code != 200:
            print(f"❌ CSV upload failed: {response.text}")
            return False
        
        data = response.json()
        print(f"✅ CSV upload successful!")
        print(f"   Imported: {data['imported_count']} students")
        if data.get('errors'):
            print(f"   Errors: {', '.join(data['errors'])}")
        return True
    
    except Exception as e:
        print(f"❌ CSV upload error: {str(e)}")
        return False

def verify_database():
    """Verify data was actually imported"""
    print("\n[4/5] Verifying database...")
    headers = {"Authorization": f"Bearer {requests.post(f'{BACKEND_URL}/api/auth/login', json={'username': ADMIN_USERNAME, 'password': ADMIN_PASSWORD}).json()['access_token']}"}
    
    # Get admin dashboard data
    response = requests.get(
        f"{BACKEND_URL}/api/admin/dashboard",
        headers={"Authorization": f"Bearer {get_admin_token()}"}
    )
    
    if response.status_code != 200:
        print(f"❌ Could not fetch dashboard: {response.text}")
        return False
    
    data = response.json()
    print(f"✅ Database verification:")
    print(f"   Total Students: {data['total_students']}")
    print(f"   Average GPA: {data['average_gpa']:.2f}")
    return True

def main():
    print("=" * 60)
    print("Student Performance System - Import Test Suite")
    print("=" * 60)
    
    # Step 1: Get admin token
    token = get_admin_token()
    if not token:
        print("\n❌ Failed to get admin token. Make sure backend is running!")
        return
    
    # Step 2: Test manual entry
    test_manual_entry(token)
    
    # Step 3: Test CSV upload
    test_csv_upload(token)
    
    # Step 4: Verify database
    verify_database()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
