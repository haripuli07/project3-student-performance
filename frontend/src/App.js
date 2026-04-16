import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './store/authStore';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';
import StudentDashboard from './pages/StudentDashboard';
import './App.css';

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const getCurrentUser = useAuthStore((state) => state.getCurrentUser);
  
  useEffect(() => {
    if (isAuthenticated) {
      getCurrentUser();
    }
  }, [isAuthenticated]);
  
  return (
    <Router>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        <Route path="/admin/dashboard" element={
          <PrivateRoute requiredRole="admin">
            <AdminDashboard />
          </PrivateRoute>
        } />
        
        <Route path="/student/dashboard" element={
          <PrivateRoute requiredRole="student">
            <StudentDashboard />
          </PrivateRoute>
        } />
        
        <Route path="/" element={
          isAuthenticated ? <Navigate to="/student/dashboard" /> : <Navigate to="/login" />
        } />
        
        <Route path="/unauthorized" element={
          <div className="flex items-center justify-center h-screen">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-red-600">Unauthorized</h1>
              <p className="text-gray-600 mt-2">You don't have permission to access this page</p>
            </div>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;
