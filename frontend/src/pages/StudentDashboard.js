import React, { useState, useEffect } from 'react';
import axios from 'axios';
import useAuthStore from '../store/authStore';

const StudentDashboard = () => {
  const [studentData, setStudentData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const user = useAuthStore((state) => state.user);
  const token = useAuthStore((state) => state.token);
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
  
  useEffect(() => {
    if (user?.student?.id) {
      fetchStudentData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);
  
  const fetchStudentData = async () => {
    try {
      setLoading(true);
      const headers = { Authorization: `Bearer ${token}` };
      
      const [student, hist] = await Promise.all([
        axios.get(`${API_BASE}/students/${user.student.id}`, { headers }),
        axios.get(`${API_BASE}/predictions/history/${user.student.id}`, { headers })
      ]);
      
      setStudentData(student.data);
      
      if (hist.data.length > 0) {
        setPrediction(hist.data[0]);
      }
    } catch (err) {
      setError('Failed to fetch student data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handlePredictPerformance = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(
        `${API_BASE}/predictions/predict/${user.student.id}`,
        { headers }
      );
      setPrediction(response.data);
      fetchStudentData();
    } catch (err) {
      setError('Failed to generate prediction');
      console.error(err);
    }
  };
  
  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }
  
  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };
  
  return (
    <div className="bg-gray-50 min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Welcome, {studentData?.first_name}!
        </h1>
        <p className="text-gray-600 mb-8">Student ID: {studentData?.admission_no}</p>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        {/* Current Performance Prediction */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Performance Analysis</h2>
            <button
              onClick={handlePredictPerformance}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg transition"
            >
              Generate Prediction
            </button>
          </div>
          
          {prediction ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="border-l-4 border-blue-500 pl-6">
                <p className="text-gray-600 text-sm font-semibold uppercase mb-2">Predicted GPA</p>
                <p className="text-4xl font-bold text-blue-600">{prediction.predicted_gpa.toFixed(2)}</p>
              </div>
              
              <div className={`border-l-4 pl-6 ${getRiskColor(prediction.risk_level)}`}>
                <p className="text-sm font-semibold uppercase mb-2">Risk Level</p>
                <p className="text-2xl font-bold">{prediction.risk_level.toUpperCase()}</p>
                <p className="text-sm mt-2">Score: {(prediction.risk_score * 100).toFixed(1)}%</p>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 bg-gray-50 rounded">
              <p className="text-gray-600 mb-4">No prediction available yet</p>
              <button
                onClick={handlePredictPerformance}
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg"
              >
                Generate First Prediction
              </button>
            </div>
          )}
        </div>
        
        {/* Performance Factors */}
        {prediction?.factors && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Performance Factors</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Attendance */}
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 mb-3">Attendance</h3>
                <p className="text-2xl font-bold text-blue-600">
                  {prediction.factors.attendance?.value.toFixed(1)}%
                </p>
                <p className={`text-sm mt-2 font-semibold ${
                  prediction.factors.attendance?.status === 'critical' ? 'text-red-600' :
                  prediction.factors.attendance?.status === 'warning' ? 'text-yellow-600' : 'text-green-600'
                }`}>
                  Status: {prediction.factors.attendance?.status.toUpperCase()}
                </p>
              </div>
              
              {/* Academic Performance */}
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 mb-3">Academic Performance</h3>
                <p className="text-sm text-gray-600">Current GPA: <span className="font-bold">{prediction.factors.academic_performance?.current_gpa.toFixed(2)}</span></p>
                <p className="text-sm text-gray-600 mt-1">Predicted GPA: <span className="font-bold">{prediction.factors.academic_performance?.predicted_gpa.toFixed(2)}</span></p>
                <p className={`text-sm mt-2 font-semibold ${
                  prediction.factors.academic_performance?.trend === 'improving' ? 'text-green-600' :
                  prediction.factors.academic_performance?.trend === 'declining' ? 'text-red-600' : 'text-blue-600'
                }`}>
                  Trend: {prediction.factors.academic_performance?.trend.toUpperCase()}
                </p>
              </div>
              
              {/* Assessment Balance */}
              <div className="border rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 mb-3">Assessment Balance</h3>
                <p className="text-sm text-gray-600">Internal: <span className="font-bold">{prediction.factors.assessment_balance?.internal_marks.toFixed(1)}</span></p>
                <p className="text-sm text-gray-600 mt-1">External: <span className="font-bold">{prediction.factors.assessment_balance?.external_marks.toFixed(1)}</span></p>
                <p className={`text-sm mt-2 font-semibold ${
                  prediction.factors.assessment_balance?.imbalance === 'high' ? 'text-red-600' :
                  prediction.factors.assessment_balance?.imbalance === 'moderate' ? 'text-yellow-600' : 'text-green-600'
                }`}>
                  Balance: {prediction.factors.assessment_balance?.imbalance.toUpperCase()}
                </p>
              </div>
            </div>
          </div>
        )}
        
        {/* Recommendations */}
        {prediction?.recommendations && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Recommendations</h2>
            <ul className="space-y-3">
              {prediction.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="text-green-500 mr-3 text-lg">✓</span>
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Academic Records */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Academic Records</h2>
          
          {studentData?.academic_records && studentData.academic_records.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-4">Subject</th>
                    <th className="text-left py-2 px-4">Internal</th>
                    <th className="text-left py-2 px-4">External</th>
                    <th className="text-left py-2 px-4">Total</th>
                    <th className="text-left py-2 px-4">GPA</th>
                    <th className="text-left py-2 px-4">Grade</th>
                  </tr>
                </thead>
                <tbody>
                  {studentData.academic_records.map((record) => (
                    <tr key={record.id} className="border-b hover:bg-gray-50">
                      <td className="py-2 px-4">{record.subject}</td>
                      <td className="py-2 px-4">{record.internal_marks?.toFixed(1)}</td>
                      <td className="py-2 px-4">{record.external_marks?.toFixed(1)}</td>
                      <td className="py-2 px-4 font-semibold">{record.total_marks?.toFixed(1)}</td>
                      <td className="py-2 px-4 font-semibold text-blue-600">{record.gpa?.toFixed(2)}</td>
                      <td className="py-2 px-4 font-bold">{record.grade}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-600">No academic records available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
