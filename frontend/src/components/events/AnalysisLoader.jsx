import React, { useState, useEffect } from 'react';
import { Loader2, Brain, Search, AlertTriangle, Lightbulb, FileText, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';

const AnalysisLoader = ({ agentLogs, isProcessing }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);

  const steps = [
    {
      icon: Brain,
      name: "Event Parser",
      description: "Analyzing incident details...",
      color: "text-purple-500"
    },
    {
      icon: Search,
      name: "Supplier Matcher",
      description: "Identifying affected suppliers...",
      color: "text-blue-500"
    },
    {
      icon: AlertTriangle,
      name: "Risk Analyzer",
      description: "Calculating risk scores...",
      color: "text-orange-500"
    },
    {
      icon: Lightbulb,
      name: "Recommendation Generator",
      description: "Finding alternative suppliers...",
      color: "text-green-500"
    },
    {
      icon: FileText,
      name: "Playbook Generator",
      description: "Creating action plan...",
      color: "text-indigo-500"
    }
  ];

  useEffect(() => {
    if (!isProcessing) return;

    // Smooth progress animation
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 1;
        if (newProgress >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return newProgress;
      });
    }, 200); // Complete in ~20 seconds

    return () => clearInterval(progressInterval);
  }, [isProcessing]);

  useEffect(() => {
    // Update current step based on agent logs
    if (agentLogs && agentLogs.length > 0) {
      const completedSteps = agentLogs.filter(log => log.status === 'completed').length;
      setCurrentStep(completedSteps);
    }
  }, [agentLogs]);

  if (!isProcessing) return null;

  return (
    <Card className="border-2 border-blue-500/20 bg-gradient-to-br from-blue-50 to-indigo-50">
      <CardHeader>
        <CardTitle className="flex items-center text-blue-900">
          <Loader2 className="h-5 w-5 mr-2 animate-spin text-blue-500" />
          AI Agents Analyzing Event
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-2">
            <span className="text-gray-600">Overall Progress</span>
            <span className="font-semibold text-blue-600">{progress}%</span>
          </div>
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            >
              <div className="h-full w-full animate-pulse bg-white/30" />
            </div>
          </div>
        </div>

        {/* Agent Steps */}
        <div className="space-y-3">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;
            const isPending = index > currentStep;

            return (
              <div 
                key={index}
                className={`
                  flex items-center space-x-4 p-3 rounded-lg transition-all duration-300
                  ${isActive ? 'bg-white shadow-md scale-105 border-2 border-blue-500' : ''}
                  ${isCompleted ? 'bg-white/50' : ''}
                  ${isPending ? 'opacity-50' : ''}
                `}
              >
                <div className={`
                  relative flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center
                  ${isActive ? 'bg-blue-100' : ''}
                  ${isCompleted ? 'bg-green-100' : ''}
                  ${isPending ? 'bg-gray-100' : ''}
                `}>
                  {isActive && (
                    <div className="absolute inset-0 rounded-full border-2 border-blue-500 animate-ping" />
                  )}
                  <Icon className={`
                    h-5 w-5 
                    ${isActive ? step.color : ''}
                    ${isCompleted ? 'text-green-500' : ''}
                    ${isPending ? 'text-gray-400' : ''}
                    ${isActive ? 'animate-pulse' : ''}
                  `} />
                </div>

                <div className="flex-1 min-w-0">
                  <p className={`
                    text-sm font-medium
                    ${isActive ? 'text-gray-900' : ''}
                    ${isCompleted ? 'text-gray-600' : ''}
                    ${isPending ? 'text-gray-500' : ''}
                  `}>
                    {step.name}
                  </p>
                  <p className={`
                    text-xs
                    ${isActive ? 'text-gray-600' : ''}
                    ${isCompleted ? 'text-gray-500' : ''}
                    ${isPending ? 'text-gray-400' : ''}
                  `}>
                    {isActive ? step.description : isCompleted ? 'Completed' : 'Pending'}
                  </p>
                </div>

                {isActive && (
                  <Loader2 className="h-4 w-4 text-blue-500 animate-spin flex-shrink-0" />
                )}
                {isCompleted && (
                  <div className="flex-shrink-0 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Animated particles effect */}
        <div className="relative h-16 overflow-hidden rounded-lg bg-gradient-to-r from-blue-100 to-purple-100">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="flex space-x-2">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                  style={{ animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Status message */}
        <div className="text-center">
          <p className="text-sm text-gray-600">
            {currentStep < 5 
              ? `Processing step ${currentStep + 1} of 5...` 
              : 'Finalizing analysis...'}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            This usually takes 15-30 seconds
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AnalysisLoader;