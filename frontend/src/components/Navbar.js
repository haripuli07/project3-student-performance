import React from 'react';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <span className="text-2xl font-bold text-blue-600">Excel College</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-gray-700">
              <p className="font-semibold">{user?.username}</p>
              <p className="text-sm text-gray-500 capitalize">{user?.role}</p>
            </div>
            
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
