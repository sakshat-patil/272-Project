import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Activity, Lock, User, TrendingUp, Shield, BarChart3 } from 'lucide-react';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Alert from '../components/ui/Alert';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(username, password);
    
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-indigo-900 via-blue-900 to-purple-900">
      {/* Left Side - Branding & Features */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-12 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 backdrop-blur-3xl"></div>
        
        <div className="relative z-10">
          <div className="flex items-center mb-8">
            <Activity className="h-12 w-12 text-blue-400" />
            <h1 className="text-4xl font-bold ml-3">
              Supply Chain Risk Monitor
            </h1>
          </div>
          
          <p className="text-xl text-blue-100 mb-12">
            AI-powered supply chain risk analysis and predictive insights
          </p>

          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Shield className="h-6 w-6 text-blue-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Real-time Risk Monitoring</h3>
                <p className="text-blue-200">Monitor your supply chain with live weather tracking and risk alerts</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <TrendingUp className="h-6 w-6 text-purple-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Predictive Analytics</h3>
                <p className="text-blue-200">AI-powered predictions to anticipate and prevent disruptions</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-indigo-500/20 p-3 rounded-lg">
                <BarChart3 className="h-6 w-6 text-indigo-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Multi-Agent Intelligence</h3>
                <p className="text-blue-200">Advanced AI agents analyze risks and generate actionable playbooks</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <div className="lg:hidden text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Activity className="h-10 w-10 text-blue-400" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Supply Chain Risk Monitor
            </h1>
            <p className="text-blue-200">AI-powered risk analysis</p>
          </div>

          <Card className="p-8 bg-white/95 backdrop-blur-sm shadow-2xl border-0">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h2>
              <p className="text-gray-600">Sign in to access your dashboard</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  {error}
                </Alert>
              )}

              <div>
                <label htmlFor="username" className="block text-sm font-semibold text-gray-700 mb-2">
                  Username
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="username"
                    type="text"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoComplete="username"
                    className="pl-10"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                    className="pl-10"
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 shadow-lg"
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </span>
                ) : 'Sign In'}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <Link to="/signup" className="text-blue-600 hover:text-blue-800 font-semibold transition-colors">
                  Create one now →
                </Link>
              </p>
            </div>
          </Card>

          <div className="mt-6 text-center text-sm text-white/80">
            <p>© 2025 Supply Chain Risk Monitor. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
