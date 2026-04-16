#!/usr/bin/env python
import urllib.request
import json

data = json.dumps({'username': 'admin', 'password': 'admin123'}).encode('utf-8')
req = urllib.request.Request('http://localhost:5000/api/auth/login', data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req)
    print(f'Status: {response.status}')
    print(f'Response: {response.read().decode()}')
except urllib.error.HTTPError as e:
    print(f'Error: {e.code}')
    print(f'Response: {e.read().decode()}')
except Exception as e:
    print(f'Error: {e}')
