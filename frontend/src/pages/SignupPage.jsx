import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Activity, Mail, User, Lock, UserPlus, Shield, Zap, Globe, Check, X } from 'lucide-react';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Alert from '../components/ui/Alert';

const PasswordRequirement = ({ met, text }) => (
  <div className="flex items-center gap-2 text-xs">
    {met ? (
      <Check className="w-4 h-4 text-green-600" />
    ) : (
      <X className="w-4 h-4 text-gray-400" />
    )}
    <span className={met ? 'text-green-600' : 'text-gray-500'}>{text}</span>
  </div>
);

export default function SignupPage() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    fullName: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false,
  });

  useEffect(() => {
    const password = formData.password;
    setPasswordStrength({
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    });
  }, [formData.password]);

  const isPasswordValid = Object.values(passwordStrength).every(Boolean);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!isPasswordValid) {
      setError('Please meet all password requirements');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    const result = await signup({
      email: formData.email,
      username: formData.username,
      password: formData.password,
      full_name: formData.full_name || null
    });

    if (result.success) {
      navigate('/');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900">
      {/* Left Side - Branding & Benefits */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-12 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 to-blue-600/20 backdrop-blur-3xl"></div>
        
        <div className="relative z-10">
          <div className="flex items-center mb-8">
            <Activity className="h-12 w-12 text-purple-400" />
            <h1 className="text-4xl font-bold ml-3">
              Supply Chain Risk Monitor
            </h1>
          </div>
          
          <p className="text-xl text-purple-100 mb-12">
            Join thousands of companies protecting their supply chains with AI
          </p>

          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="bg-purple-500/20 p-3 rounded-lg">
                <Shield className="h-6 w-6 text-purple-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Enterprise Security</h3>
                <p className="text-purple-200">Bank-level encryption and security for your sensitive data</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-blue-500/20 p-3 rounded-lg">
                <Zap className="h-6 w-6 text-blue-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Instant Insights</h3>
                <p className="text-purple-200">Get started in minutes with automatic risk detection</p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="bg-indigo-500/20 p-3 rounded-lg">
                <Globe className="h-6 w-6 text-indigo-300" />
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">Global Coverage</h3>
                <p className="text-purple-200">Monitor suppliers worldwide with real-time weather and risk data</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Signup Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <div className="lg:hidden text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Activity className="h-10 w-10 text-purple-400" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Supply Chain Risk Monitor
            </h1>
            <p className="text-purple-200">AI-powered risk analysis</p>
          </div>

          <Card className="p-8 bg-white/95 backdrop-blur-sm shadow-2xl border-0">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full mb-4">
                <UserPlus className="h-8 w-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Get Started</h2>
              <p className="text-gray-600">Create your account in seconds</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  {error}
                </Alert>
              )}

              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="you@company.com"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    autoComplete="email"
                    className="pl-10"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="username" className="block text-sm font-semibold text-gray-700 mb-2">
                  Username
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Choose a username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    autoComplete="username"
                    className="pl-10"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="full_name" className="block text-sm font-semibold text-gray-700 mb-2">
                  Full Name <span className="text-gray-400 font-normal">(Optional)</span>
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="full_name"
                    name="full_name"
                    type="text"
                    placeholder="Your full name"
                    value={formData.full_name}
                    onChange={handleChange}
                    autoComplete="name"
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
                    name="password"
                    type="password"
                    placeholder="Create a strong password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    autoComplete="new-password"
                    className="pl-10"
                  />
                </div>
                {formData.password && (
                  <div className="mt-3 p-3 bg-gray-50 rounded-lg space-y-2">
                    <p className="text-xs font-semibold text-gray-700 mb-2">Password Requirements:</p>
                    <PasswordRequirement met={passwordStrength.length} text="At least 8 characters" />
                    <PasswordRequirement met={passwordStrength.uppercase} text="One uppercase letter" />
                    <PasswordRequirement met={passwordStrength.lowercase} text="One lowercase letter" />
                    <PasswordRequirement met={passwordStrength.number} text="One number" />
                    <PasswordRequirement met={passwordStrength.special} text="One special character (!@#$%^&*...)" />
                  </div>
                )}
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-semibold text-gray-700 mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    autoComplete="new-password"
                    className="pl-10"
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 shadow-lg mt-6"
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating account...
                  </span>
                ) : 'Create Account'}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Already have an account?{' '}
                <Link to="/login" className="text-purple-600 hover:text-purple-800 font-semibold transition-colors">
                  Sign in →
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
