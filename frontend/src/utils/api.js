const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Authentication
const getAuthHeader = () => ({
  'Authorization': `Bearer ${localStorage.getItem('token')}`,
  'Content-Type': 'application/json'
});

export const api = {
  // Auth endpoints
  login: (credentials) => fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  }),
  
  register: (userData) => fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  }),
  
  // Student endpoints
  getStudents: () => fetch(`${API_BASE}/students`, { headers: getAuthHeader() }),
  getStudent: (id) => fetch(`${API_BASE}/students/${id}`, { headers: getAuthHeader() }),
  
  // Prediction endpoints
  predictPerformance: (studentId) => fetch(`${API_BASE}/predictions/predict/${studentId}`, { 
    headers: getAuthHeader() 
  }),
  
  getPredictionHistory: (studentId) => fetch(`${API_BASE}/predictions/history/${studentId}`, { 
    headers: getAuthHeader() 
  }),
  
  // Admin endpoints
  getDashboard: () => fetch(`${API_BASE}/admin/dashboard`, { headers: getAuthHeader() }),
  getRiskDistribution: () => fetch(`${API_BASE}/admin/analytics/risk-distribution`, { 
    headers: getAuthHeader() 
  }),
};
