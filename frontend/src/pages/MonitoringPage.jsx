import { useState, useEffect } from 'react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Spinner from '../components/ui/Spinner';
import Alert from '../components/ui/Alert';

const MonitoringPage = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchMonitoringData = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/monitoring/dashboard');
      if (!response.ok) throw new Error('Failed to fetch monitoring data');
      const data = await response.json();
      setDashboardData(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMonitoringData();
  }, []);

  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(fetchMonitoringData, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const getHealthColor = (status) => {
    switch (status) {
      case 'HEALTHY': return 'default';
      case 'DEGRADED': return 'secondary';
      case 'UNHEALTHY': return 'destructive';
      default: return 'outline';
    }
  };

  const getHealthIcon = (status) => {
    switch (status) {
      case 'HEALTHY': return '';
      case 'DEGRADED': return '';
      case 'UNHEALTHY': return '';
      default: return '';
    }
  };

  const getEventLevelColor = (level) => {
    switch (level) {
      case 'ERROR': return 'destructive';
      case 'WARNING': return 'secondary';
      case 'INFO': return 'default';
      default: return 'outline';
    }
  };

  const formatUptime = (seconds) => {
    if (!seconds) return '0s';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) return `${hours}h ${minutes}m`;
    if (minutes > 0) return `${minutes}m ${secs}s`;
    return `${secs}s`;
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert variant="error">
          <p>Error loading monitoring data: {error}</p>
          <button 
            onClick={() => {
              setLoading(true);
              fetchMonitoringData();
            }}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Retry
          </button>
        </Alert>
      </div>
    );
  }

  const { health, summary, top_endpoints, slowest_endpoints, recent_events } = dashboardData || {};

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">System Monitoring</h1>
          <p className="text-gray-600 mt-1">Real-time API performance and health monitoring</p>
        </div>
        <div className="flex gap-3 items-center">
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded"
            />
            Auto-refresh (10s)
          </label>
          <button
            onClick={fetchMonitoringData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Refresh Now
          </button>
        </div>
      </div>

      {/* Health Status Card */}
      <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-700 mb-2">System Health</h2>
            <div className="flex items-center gap-3">
              <span className="text-4xl">{getHealthIcon(health?.status)}</span>
              <div>
                <Badge variant={getHealthColor(health?.status)} className="text-lg px-4 py-1">
                  {health?.status || 'UNKNOWN'}
                </Badge>
                <p className="text-sm text-gray-600 mt-1">
                  Error Rate: {health?.error_rate?.toFixed(2)}%
                </p>
              </div>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">System Uptime</p>
            <p className="text-3xl font-bold text-blue-600">
              {formatUptime(summary?.uptime_seconds)}
            </p>
          </div>
        </div>
      </Card>

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-white">
          <div className="text-center">
            <p className="text-sm text-gray-600">Total API Calls</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">
              {summary?.total_calls?.toLocaleString() || 0}
            </p>
          </div>
        </Card>
        
        <Card className="bg-white">
          <div className="text-center">
            <p className="text-sm text-gray-600">Total Errors</p>
            <p className="text-3xl font-bold text-red-600 mt-2">
              {summary?.total_errors?.toLocaleString() || 0}
            </p>
          </div>
        </Card>
        
        <Card className="bg-white">
          <div className="text-center">
            <p className="text-sm text-gray-600">Error Rate</p>
            <p className="text-3xl font-bold text-yellow-600 mt-2">
              {summary?.error_rate?.toFixed(2)}%
            </p>
          </div>
        </Card>
        
        <Card className="bg-white">
          <div className="text-center">
            <p className="text-sm text-gray-600">Uptime</p>
            <p className="text-3xl font-bold text-green-600 mt-2">
              {formatUptime(summary?.uptime_seconds)}
            </p>
          </div>
        </Card>
      </div>

      {/* Top Endpoints and Slowest Endpoints */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Endpoints */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Called Endpoints</h3>
          <div className="space-y-3">
            {top_endpoints && top_endpoints.length > 0 ? (
              top_endpoints.map((endpoint, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 text-sm">{endpoint.endpoint}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      Avg: {endpoint.avg_time_ms?.toFixed(0) || 0}ms
                    </p>
                  </div>
                  <div className="text-right">
                    <Badge variant="default" className="text-lg">
                      {endpoint.calls || endpoint.total_calls}
                    </Badge>
                    <p className="text-xs text-gray-500 mt-1">calls</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No data yet</p>
            )}
          </div>
        </Card>

        {/* Slowest Endpoints */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Slowest Endpoints</h3>
          <div className="space-y-3">
            {slowest_endpoints && slowest_endpoints.length > 0 ? (
              slowest_endpoints.map((endpoint, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 text-sm">{endpoint.endpoint}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {endpoint.calls || endpoint.total_calls || 0} calls
                    </p>
                  </div>
                  <div className="text-right">
                    <Badge variant="secondary" className="text-lg">
                      {endpoint.avg_time_ms?.toFixed(0) || endpoint.avg_response_time?.toFixed(0) || 0}ms
                    </Badge>
                    <p className="text-xs text-gray-500 mt-1">avg time</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-4">No data yet</p>
            )}
          </div>
        </Card>
      </div>

      {/* Recent Events Log */}
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Events & Logs</h3>
        <div className="bg-gray-900 rounded-lg p-4 max-h-96 overflow-y-auto">
          {recent_events && recent_events.length > 0 ? (
            <div className="space-y-2 font-mono text-sm">
              {recent_events.map((event, idx) => (
                <div key={idx} className="flex items-start gap-3 text-gray-300">
                  <span className="text-gray-500 text-xs">
                    {formatTime(event.timestamp)}
                  </span>
                  <Badge variant={getEventLevelColor(event.level)} className="text-xs">
                    {event.level}
                  </Badge>
                  <span className="text-blue-400">[{event.event_type}]</span>
                  <span className="flex-1">{event.message}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">No events logged yet</p>
          )}
        </div>
      </Card>

      {/* API Documentation */}
      <Card className="bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Monitoring Endpoints</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="bg-white p-3 rounded">
            <code className="text-blue-600">GET /api/monitoring/health</code>
            <p className="text-gray-600 mt-1">System health status</p>
          </div>
          <div className="bg-white p-3 rounded">
            <code className="text-blue-600">GET /api/monitoring/metrics</code>
            <p className="text-gray-600 mt-1">All metrics and statistics</p>
          </div>
          <div className="bg-white p-3 rounded">
            <code className="text-blue-600">GET /api/monitoring/api-stats</code>
            <p className="text-gray-600 mt-1">Per-endpoint statistics</p>
          </div>
          <div className="bg-white p-3 rounded">
            <code className="text-blue-600">GET /api/monitoring/events</code>
            <p className="text-gray-600 mt-1">System events and logs</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default MonitoringPage;
