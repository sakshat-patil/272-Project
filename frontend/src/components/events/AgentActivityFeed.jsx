import React, { useEffect, useState } from 'react';
import { CheckCircle2, Clock, Loader2, XCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';

const AgentActivityFeed = ({ agentLogs, isProcessing }) => {
  const [displayedLogs, setDisplayedLogs] = useState([]);

  useEffect(() => {
    if (agentLogs && agentLogs.length > 0) {
      // Simulate progressive display of logs
      setDisplayedLogs([]);
      agentLogs.forEach((log, index) => {
        setTimeout(() => {
          setDisplayedLogs(prev => [...prev, log]);
        }, index * 300);
      });
    }
  }, [agentLogs]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case 'processing':
        return <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  if (!isProcessing && (!agentLogs || agentLogs.length === 0)) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Agent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {displayedLogs.map((log, index) => (
            <div
              key={index}
              className="flex items-start space-x-3 animate-in fade-in slide-in-from-left-5"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="flex-shrink-0 mt-1">
                {getStatusIcon(log.status)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  {log.agent}
                </p>
                {log.output && (
                  <p className="text-sm text-gray-600 mt-1">
                    {log.output}
                  </p>
                )}
                {log.error && (
                  <p className="text-sm text-red-600 mt-1">
                    Error: {log.error}
                  </p>
                )}
                {log.timestamp && (
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </p>
                )}
              </div>
            </div>
          ))}

          {isProcessing && displayedLogs.length === 0 && (
            <div className="flex items-center space-x-3">
              <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
              <p className="text-sm text-gray-600">
                Initializing agent analysis...
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default AgentActivityFeed;