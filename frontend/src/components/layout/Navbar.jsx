import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Building2, Activity, LogOut, User } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import Button from '../ui/Button';

const Navbar = () => {
  const location = useLocation();
  const auth = useAuth();
  const { user, logout } = auth || { user: null, logout: () => {} };
  
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <Activity className="h-8 w-8 text-primary" />
              <span className="ml-2 text-xl font-bold text-gray-900">
                Supply Chain Risk Monitor
              </span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/'
                  ? 'bg-primary text-white'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Building2 className="inline-block h-4 w-4 mr-1" />
              Organizations
            </Link>
            
            {user && (
              <div className="flex items-center space-x-3 ml-4 pl-4 border-l border-gray-300">
                <div className="flex items-center space-x-2 text-sm">
                  <User className="h-4 w-4 text-gray-600" />
                  <span className="text-gray-700 font-medium">
                    {user.full_name || user.username}
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={logout}
                  className="flex items-center space-x-1"
                >
                  <LogOut className="h-4 w-4" />
                  <span>Logout</span>
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;