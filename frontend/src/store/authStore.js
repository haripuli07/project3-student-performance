import { create } from 'zustand';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// Initialize axios with token from localStorage if it exists
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  
  login: async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        username,
        password
      });
      
      const { access_token, user_id, role, username: uname } = response.data;
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      set({
        user: { id: user_id, username: uname, role },
        token: access_token,
        isAuthenticated: true
      });
      
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
  
  register: async (userData) => {
    try {
      const response = await axios.post(`${API_BASE}/auth/register`, userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
  
  logout: () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    set({
      user: null,
      token: null,
      isAuthenticated: false
    });
  },
  
  getCurrentUser: async () => {
    try {
      const response = await axios.get(`${API_BASE}/auth/me`);
      set({ user: response.data });
      return response.data;
    } catch (error) {
      set({ isAuthenticated: false });
      throw error;
    }
  }
}));

export default useAuthStore;
