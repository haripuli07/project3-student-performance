import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import useAuthStore from '../store/authStore';
import DataImport from './DataImport';

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [riskDistribution, setRiskDistribution] = useState(null);
  const [topPerformers, setTopPerformers] = useState([]);
  const [atRiskStudents, setAtRiskStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('analytics');
  
  const token = useAuthStore((state) => state.token);
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
  
  useEffect(() => {
    fetchDashboardData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const headers = { Authorization: `Bearer ${token}` };
      
      const [dashboard, risk, top, atRisk] = await Promise.all([
        axios.get(`${API_BASE}/admin/dashboard`, { headers }),
        axios.get(`${API_BASE}/admin/analytics/risk-distribution`, { headers }),
        axios.get(`${API_BASE}/admin/analytics/top-performers`, { headers }),
        axios.get(`${API_BASE}/admin/analytics/at-risk-students`, { headers })
      ]);
      
      setDashboardData(dashboard.data);
      setRiskDistribution(risk.data);
      setTopPerformers(top.data);
      setAtRiskStudents(atRisk.data);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }
  
  const riskData = riskDistribution ? [
    { name: 'Low Risk', value: riskDistribution.low, color: '#10b981' },
    { name: 'Medium Risk', value: riskDistribution.medium, color: '#f59e0b' },
    { name: 'High Risk', value: riskDistribution.high, color: '#ef4444' }
  ] : [];
  
  return (
    <div className="bg-gray-50 min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">Admin Dashboard</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 mb-8">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-6 py-3 font-medium ${
              activeTab === 'analytics'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            📊 Analytics
          </button>
          <button
            onClick={() => setActiveTab('import')}
            className={`px-6 py-3 font-medium ${
              activeTab === 'import'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            📤 Data Import
          </button>
        </div>
        
        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
        <>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-semibold uppercase">Total Students</h3>
            <p className="text-4xl font-bold text-blue-600 mt-2">
              {dashboardData?.total_students || 0}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-semibold uppercase">Total Predictions</h3>
            <p className="text-4xl font-bold text-green-600 mt-2">
              {dashboardData?.total_predictions || 0}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-semibold uppercase">High Risk</h3>
            <p className="text-4xl font-bold text-red-600 mt-2">
              {riskDistribution?.high || 0}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-500 text-sm font-semibold uppercase">Average GPA</h3>
            <p className="text-4xl font-bold text-purple-600 mt-2">
              {dashboardData?.average_gpa?.toFixed(2) || '0.00'}
            </p>
          </div>
        </div>
        
        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Risk Distribution Pie Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Risk Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {riskData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          {/* Top Performers */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Top Performers</h2>
            <div className="space-y-3">
              {topPerformers.slice(0, 5).map((student, index) => (
                <div key={student.student_id} className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-800">{index + 1}. {student.name}</p>
                    <p className="text-sm text-gray-500">{student.admission_no}</p>
                  </div>
                  <p className="text-lg font-bold text-green-600">{student.average_gpa}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* At-Risk Students */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">At-Risk Students Requiring Intervention</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-4">Student Name</th>
                  <th className="text-left py-2 px-4">Admission No.</th>
                  <th className="text-left py-2 px-4">Risk Score</th>
                  <th className="text-left py-2 px-4">Key Factors</th>
                  <th className="text-left py-2 px-4">Recommendations</th>
                </tr>
              </thead>
              <tbody>
                {atRiskStudents.slice(0, 5).map((student) => (
                  <tr key={student.student_id} className="border-b hover:bg-gray-50">
                    <td className="py-2 px-4">{student.name}</td>
                    <td className="py-2 px-4">{student.admission_no}</td>
                    <td className="py-2 px-4">
                      <span className="bg-red-100 text-red-800 px-2 py-1 rounded">
                        {student.risk_score.toFixed(2)}
                      </span>
                    </td>
                    <td className="py-2 px-4 text-sm">
                      {student.factors?.attendance?.status === 'critical' && (
                        <span className="block text-red-600">Low Attendance</span>
                      )}
                      {student.factors?.academic_performance?.trend === 'declining' && (
                        <span className="block text-red-600">Declining Performance</span>
                      )}
                    </td>
                    <td className="py-2 px-4 text-sm">
                      {student.recommendations?.slice(0, 2).map((rec, idx) => (
                        <div key={idx}>{rec}</div>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        </>
        )}
        
        {/* Import Tab */}
        {activeTab === 'import' && (
          <DataImport />
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
