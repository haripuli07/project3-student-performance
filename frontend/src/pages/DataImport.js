import React, { useState } from 'react';
import axios from 'axios';

const DataImport = () => {
  const [activeTab, setActiveTab] = useState('csv');
  const [csvFile, setCsvFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  
  // Manual entry form state
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    admission_no: '',
    email: '',
    username: '',
    exam_score: '',
    previous_scores: '',
    department: 'Information Technology',
    semester: '1',
    section: 'A',
    subject: 'Performance Analytics'
  });

  const handleCsvUpload = async (e) => {
    e.preventDefault();
    
    if (!csvFile) {
      setMessage('Please select a CSV file');
      setMessageType('error');
      return;
    }

    setLoading(true);
    setMessage('');

    const formDataToSend = new FormData();
    formDataToSend.append('file', csvFile);

    try {
      const response = await axios.post('http://localhost:5000/api/import/upload-csv', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setMessage(`✓ ${response.data.message} (${response.data.imported_count}/${response.data.total_rows})`);
      setMessageType('success');
      setCsvFile(null);
      
      if (response.data.errors && response.data.errors.length > 0) {
        setMessage(`${response.data.message}. Errors: ${response.data.errors.join('; ')}`);
        setMessageType('warning');
      }
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || 'Upload failed'}`);
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  const handleManualEntry = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:5000/api/import/manual-entry', formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setMessage(`✓ ${response.data.message}`);
      setMessageType('success');
      
      // Reset form
      setFormData({
        first_name: '',
        last_name: '',
        admission_no: '',
        email: '',
        username: '',
        exam_score: '',
        previous_scores: '',
        department: 'Information Technology',
        semester: '1',
        section: 'A',
        subject: 'Performance Analytics'
      });
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.message || 'Registration failed'}`);
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Data Import & Registration</h2>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          messageType === 'success' ? 'bg-green-100 text-green-800 border border-green-300' :
          messageType === 'error' ? 'bg-red-100 text-red-800 border border-red-300' :
          'bg-yellow-100 text-yellow-800 border border-yellow-300'
        }`}>
          {message}
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('csv')}
          className={`px-6 py-3 font-medium ${
            activeTab === 'csv'
              ? 'border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          📤 Bulk CSV Upload
        </button>
        <button
          onClick={() => setActiveTab('manual')}
          className={`px-6 py-3 font-medium ${
            activeTab === 'manual'
              ? 'border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          ✍️ Manual Entry
        </button>
      </div>

      {/* CSV Upload Tab */}
      {activeTab === 'csv' && (
        <form onSubmit={handleCsvUpload} className="space-y-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-800">
              <strong>📋 Expected CSV Columns:</strong> Hours_Studied, Attendance, Previous_Scores, Exam_Score, and other performance factors. The system will automatically create student accounts and academic records.
            </p>
          </div>

          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition">
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setCsvFile(e.target.files[0])}
              className="hidden"
              id="csvFile"
            />
            <label htmlFor="csvFile" className="cursor-pointer">
              <div className="text-4xl mb-2">📁</div>
              <p className="text-gray-700 font-medium">
                {csvFile ? csvFile.name : 'Click to select CSV file or drag & drop'}
              </p>
              <p className="text-gray-500 text-sm mt-1">CSV format only</p>
            </label>
          </div>

          <button
            type="submit"
            disabled={!csvFile || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
          >
            {loading ? 'Uploading...' : 'Upload & Import Students'}
          </button>
        </form>
      )}

      {/* Manual Entry Tab */}
      {activeTab === 'manual' && (
        <form onSubmit={handleManualEntry} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            {/* First Name */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                First Name *
              </label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="John"
              />
            </div>

            {/* Last Name */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Last Name *
              </label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="Doe"
              />
            </div>

            {/* Admission Number */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Admission Number *
              </label>
              <input
                type="text"
                name="admission_no"
                value={formData.admission_no}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="22EGIT001"
              />
            </div>

            {/* Username */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Username (optional)
              </label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="john_doe"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Email (optional)
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="john@excel.edu"
              />
            </div>

            {/* Department */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Department
              </label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            {/* Previous Scores */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Previous Scores (0-100) *
              </label>
              <input
                type="number"
                name="previous_scores"
                value={formData.previous_scores}
                onChange={handleInputChange}
                required
                min="0"
                max="100"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="75"
              />
            </div>

            {/* Exam Score */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Exam Score (0-100) *
              </label>
              <input
                type="number"
                name="exam_score"
                value={formData.exam_score}
                onChange={handleInputChange}
                required
                min="0"
                max="100"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="85"
              />
            </div>

            {/* Semester */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Semester
              </label>
              <select
                name="semester"
                value={formData.semester}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              >
                {[1, 2, 3, 4, 5, 6, 7, 8].map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>

            {/* Section */}
            <div>
              <label className="block text-gray-700 font-medium mb-2">
                Section
              </label>
              <select
                name="section"
                value={formData.section}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              >
                {['A', 'B', 'C', 'D'].map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={!formData.first_name || !formData.last_name || !formData.admission_no || !formData.exam_score || !formData.previous_scores || loading}
            className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
          >
            {loading ? 'Registering...' : '✍️ Register Student'}
          </button>
        </form>
      )}
    </div>
  );
};

export default DataImport;
