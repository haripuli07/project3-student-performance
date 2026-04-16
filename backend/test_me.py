#!/usr/bin/env python
import urllib.request
import json

# Use the token from login
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NjMzMzgyOCwianRpIjoiNDIwMzZlMjItOWE5Zi00OGRmLThlMDEtMjQ5YjRmZTIwMjIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NzYzMzM4MjgsImNzcmYiOiI3MjE0YmFiMi1iMGNhLTQwZGYtYWM3ZS05OTk3ZGI4NWUyY2UiLCJleHAiOjE3Nzg5MjU4Mjh9.ag7_rkAlCiA_QlqQ_ujhEzPlaoROv6O4pFGAb0_Mo2Y"

req = urllib.request.Request('http://localhost:5000/api/auth/me', headers={
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
})

try:
    response = urllib.request.urlopen(req)
    print(f'Status: {response.status}')
    print(f'Response: {response.read().decode()}')
except urllib.error.HTTPError as e:
    print(f'Error: {e.code}')
    print(f'Response: {e.read().decode()}')
except Exception as e:
    print(f'Error: {e}')
