import React, { useState, useEffect } from 'react';
import { AlertTriangle, Cloud, Thermometer, Wind, Droplets, MapPin, Clock, TrendingUp } from 'lucide-react';
import Badge from '../ui/Badge';
import { Card } from '../ui/Card';
import { formatDistanceToNow } from '../../utils/formatters';

/**
 * Live Weather Feed Component
 * Polls real-time weather data from Open-Meteo API via backend
 * Shows current conditions and severe weather alerts for all suppliers
 */
export default function LiveWeatherFeed({ organizationId, onViewEvent }) {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [workerStatus, setWorkerStatus] = useState(null);
  const [autoEvents, setAutoEvents] = useState([]);

    // Fetch weather data
  const fetchWeather = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/weather/organization/${organizationId}/`);
      if (!response.ok) throw new Error('Failed to fetch weather data');
      const data = await response.json();
      setWeatherData(data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      console.error('Error fetching weather:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch worker status
  const fetchWorkerStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/weather/worker/status/');
      if (response.ok) {
        const data = await response.json();
        setWorkerStatus(data);
      }
    } catch (err) {
      console.error('Error fetching worker status:', err);
    }
  };

  // Fetch recent auto-generated events
  const fetchAutoEvents = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/events/organization/${organizationId}/?limit=5`);
      if (response.ok) {
        const data = await response.json();
        // Filter for auto-detected weather events
        const weatherEvents = data.filter(e => 
          e.event_type === 'weather_disruption' && 
          e.event_data?.auto_detected === true
        );
        setAutoEvents(weatherEvents);
      }
    } catch (err) {
      console.error('Error fetching auto events:', err);
    }
  };

  // Poll every 30 seconds (weather doesn't change that fast)
  useEffect(() => {
    fetchWeather();
    fetchWorkerStatus();
    fetchAutoEvents();
    
    const interval = setInterval(() => {
      fetchWeather();
      fetchWorkerStatus();
      fetchAutoEvents();
    }, 30000);
    
    return () => clearInterval(interval);
  }, [organizationId]);

  // Trigger analysis for severe weather
  const analyzeWeatherAlerts = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `http://localhost:8000/api/weather/organization/${organizationId}/analyze-alerts`,
        { method: 'POST' }
      );
      if (!response.ok) throw new Error('Failed to analyze weather alerts');
      const result = await response.json();
      alert(`Created ${result.events_created} weather event(s) for analysis`);
      // Refresh weather data
      await fetchWeather();
    } catch (err) {
      console.error('Error analyzing alerts:', err);
      alert('Failed to analyze weather alerts');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !weatherData) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading weather data...</span>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6">
        <div className="text-red-600">
          <AlertTriangle className="inline mr-2" size={20} />
          {error}
        </div>
      </Card>
    );
  }

  if (!weatherData) return null;

  const { 
    total_suppliers, 
    monitored_suppliers, 
    total_alerts,
    critical_alerts = [],
    high_alerts = [],
    moderate_alerts = [],
    weather_data = [] 
  } = weatherData;

  // Get severity badge color
  const getSeverityColor = (severity) => {
    if (severity >= 5) return 'bg-red-600 text-white';
    if (severity >= 4) return 'bg-orange-500 text-white';
    if (severity >= 3) return 'bg-yellow-500 text-white';
    return 'bg-blue-500 text-white';
  };

  // Get alert icon
  const getAlertIcon = (type) => {
    switch (type) {
      case 'extreme_heat':
      case 'extreme_cold':
        return <Thermometer size={16} />;
      case 'heavy_rain':
        return <Droplets size={16} />;
      case 'severe_wind':
      case 'strong_wind':
        return <Wind size={16} />;
      default:
        return <Cloud size={16} />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with stats and worker status */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <Cloud className="text-blue-600" />
            Live Weather Monitoring
            {workerStatus && workerStatus.running && (
              <span className="flex items-center gap-1 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                <span className="animate-pulse">●</span> Auto-monitoring active
              </span>
            )}
          </h3>
          <p className="text-sm text-gray-600 flex items-center gap-2 mt-1">
            <Clock size={14} />
            Last update: {lastUpdate ? formatDistanceToNow(lastUpdate) : 'Never'}
          </p>
        </div>
        
        <div className="flex gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-800">{monitored_suppliers}</div>
            <div className="text-xs text-gray-600">Suppliers Monitored</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${total_alerts > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {total_alerts}
            </div>
            <div className="text-xs text-gray-600">Active Alerts</div>
          </div>
        </div>
      </div>

      {/* Auto-generated events notification */}
      {autoEvents.length > 0 && (
        <Card className="p-4 bg-blue-50 border-blue-200">
          <div>
            <h4 className="font-semibold text-blue-900 flex items-center gap-2 mb-3">
              <AlertTriangle className="text-blue-600" size={20} />
              Recent Auto-Detected Weather Events ({autoEvents.length})
            </h4>
            <div className="space-y-2">
              {autoEvents.slice(0, 3).map((event) => (
                <div 
                  key={event.id} 
                  className="text-sm bg-white p-3 rounded border border-blue-200 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => onViewEvent && onViewEvent(event.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{event.description}</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Detected {formatDistanceToNow(new Date(event.created_at))} • 
                        Status: <span className={`font-semibold ${
                          event.processing_status === 'completed' ? 'text-green-600' : 
                          event.processing_status === 'processing' ? 'text-blue-600' :
                          event.processing_status === 'failed' ? 'text-red-600' : 'text-gray-600'
                        }`}>{event.processing_status}</span>
                      </p>
                      {event.processing_status === 'completed' && (
                        <p className="text-xs text-blue-600 mt-1 font-medium">
                          Click to view full analysis →
                        </p>
                      )}
                    </div>
                    <Badge className="bg-blue-600 text-white ml-2">
                      Severity {event.severity}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Alert summary */}
      {total_alerts > 0 && (
        <Card className="p-4 bg-red-50 border-red-200">
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-semibold text-red-900 flex items-center gap-2">
                <AlertTriangle className="text-red-600" size={20} />
                Severe Weather Alerts Detected
              </h4>
              <div className="mt-2 space-x-4 text-sm">
                {critical_alerts.length > 0 && (
                  <span className="text-red-700">
                    🔴 {critical_alerts.length} Critical
                  </span>
                )}
                {high_alerts.length > 0 && (
                  <span className="text-orange-700">
                    🟠 {high_alerts.length} High
                  </span>
                )}
                {moderate_alerts.length > 0 && (
                  <span className="text-yellow-700">
                    🟡 {moderate_alerts.length} Moderate
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={analyzeWeatherAlerts}
              disabled={loading}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 text-sm font-medium"
            >
              Analyze & Create Events
            </button>
          </div>
        </Card>
      )}

      {/* Detailed alerts */}
      {(critical_alerts.length > 0 || high_alerts.length > 0) && (
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-900">High Priority Alerts</h4>
          {[...critical_alerts, ...high_alerts].map((alert, idx) => (
            <Card key={idx} className="p-4 border-l-4 border-red-500">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    {getAlertIcon(alert.type)}
                    <span className="font-semibold text-gray-900">{alert.message}</span>
                    <Badge className={getSeverityColor(alert.severity)}>
                      Severity {alert.severity}
                    </Badge>
                  </div>
                  <div className="text-sm text-gray-700 mb-1">
                    <MapPin size={14} className="inline mr-1" />
                    <strong>{alert.supplier}</strong> - {alert.location}
                  </div>
                  <p className="text-sm text-gray-600">{alert.description}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    <TrendingUp size={12} className="inline mr-1" />
                    Impact: {alert.impact}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* All supplier weather cards */}
      <div>
        <h4 className="font-semibold text-gray-900 mb-3">All Suppliers Weather Status</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {weather_data.map((weather) => (
            <Card key={weather.supplier_id} className={`p-4 ${weather.alerts.length > 0 ? 'border-yellow-400 border-2' : ''}`}>
              <div className="space-y-2">
                <div className="flex justify-between items-start">
                  <div>
                    <h5 className="font-semibold text-gray-900">{weather.supplier_name}</h5>
                    <p className="text-xs text-gray-600 flex items-center gap-1">
                      <MapPin size={12} />
                      {weather.location}
                    </p>
                  </div>
                  {weather.alerts.length > 0 && (
                    <Badge className="bg-yellow-500 text-white">
                      {weather.alerts.length} Alert{weather.alerts.length > 1 ? 's' : ''}
                    </Badge>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="flex items-center gap-1">
                    <Thermometer size={14} className="text-red-500" />
                    <span>{weather.temperature}°C</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Wind size={14} className="text-blue-500" />
                    <span>{weather.wind_speed} km/h</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Droplets size={14} className="text-blue-600" />
                    <span>{weather.precipitation} mm</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Cloud size={14} className="text-gray-500" />
                    <span className="text-xs truncate">
                      {weather.condition || 'Unknown'}
                    </span>
                  </div>
                </div>

                {weather.alerts.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-200">
                    <div className="text-xs space-y-1">
                      {weather.alerts.map((alert, idx) => (
                        <div key={idx} className="flex items-start gap-1">
                          <AlertTriangle size={12} className="text-yellow-600 mt-0.5" />
                          <span className="text-gray-700">{alert.message}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* No suppliers message */}
      {weather_data.length === 0 && (
        <Card className="p-8 text-center text-gray-500">
          <Cloud size={48} className="mx-auto mb-4 text-gray-400" />
          <p>No supplier location data available for weather monitoring</p>
        </Card>
      )}
    </div>
  );
}

// Helper function to interpret weather codes
function interpretWeatherCode(code) {
  const codes = {
    0: 'Clear',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Rime fog',
    51: 'Light drizzle',
    53: 'Drizzle',
    55: 'Heavy drizzle',
    61: 'Light rain',
    63: 'Rain',
    65: 'Heavy rain',
    71: 'Light snow',
    73: 'Snow',
    75: 'Heavy snow',
    77: 'Snow grains',
    80: 'Rain showers',
    81: 'Heavy showers',
    82: 'Violent showers',
    85: 'Snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm + hail',
    99: 'Heavy thunderstorm'
  };
  return codes[code] || 'Unknown';
}
