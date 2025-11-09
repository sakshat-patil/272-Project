import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';
import Button from '../components/ui/Button';

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">
          Page Not Found
        </h2>
        <p className="text-gray-600 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Button onClick={() => navigate('/')}>
          <Home className="h-4 w-4 mr-2" />
          Back to Home
        </Button>
      </div>
    </div>
  );
};

export default NotFoundPage;