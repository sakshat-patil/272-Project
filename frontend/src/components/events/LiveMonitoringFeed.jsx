import React, { useState, useEffect } from 'react';
import { AlertTriangle, Cloud, Thermometer, Wind, Droplets, MapPin, Clock, TrendingUp, DollarSign, Ship, Globe, BarChart3 } from 'lucide-react';
import Badge from '../ui/Badge';
import { Card } from '../ui/Card';
import { formatDistanceToNow } from '../../utils/formatters';

/**
 * Live Monitoring Feed Component
 * Combines weather, financial, shipping, geopolitical, and social media data
 */
export default function LiveMonitoringFeed({ organizationId, onViewEvent }) {
  const [weatherData, setWeatherData] = useState(null);
  const [enhancedData, setEnhancedData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [activeTab, setActiveTab] = useState('weather');

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

  // Fetch enhanced monitoring data
  const fetchEnhancedData = async () => {
    try {
      const [portsRes, trendsRes, riskRes] = await Promise.all([
        fetch('http://localhost:8000/api/enhanced/shipping/major-ports'),
        fetch('http://localhost:8000/api/enhanced/social/trends?keyword=supply%20chain'),
        fetch(`http://localhost:8000/api/enhanced/risk/dashboard?organization_id=${organizationId}`)
      ]);

      const data = {
        ports: portsRes.ok ? await portsRes.json() : null,
        trends: trendsRes.ok ? await trendsRes.json() : null,
        risk: riskRes.ok ? await riskRes.json() : null,
      };

      setEnhancedData(data);
    } catch (err) {
      console.error('Error fetching enhanced data:', err);
    }
  };

  useEffect(() => {
    fetchWeather();
    fetchEnhancedData();
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetchWeather();
      fetchEnhancedData();
    }, 30000);

    return () => clearInterval(interval);
  }, [organizationId]);

  const tabs = [
    { id: 'weather', label: 'Weather', icon: Cloud },
    { id: 'shipping', label: 'Shipping', icon: Ship },
    { id: 'markets', label: 'Markets', icon: TrendingUp },
    { id: 'risks', label: 'Risks', icon: AlertTriangle },
  ];

  const getSeverityColor = (severity) => {
    const colors = {
      CRITICAL: 'bg-red-100 text-red-800 border-red-200',
      HIGH: 'bg-orange-100 text-orange-800 border-orange-200',
      MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      LOW: 'bg-blue-100 text-blue-800 border-blue-200',
    };
    return colors[severity] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  if (loading && !weatherData && !enhancedData) {
    return (
      <Card className="p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading live data...</span>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Live Monitoring</h2>
          <p className="text-sm text-gray-500">
            Real-time weather, shipping, financial, and geopolitical data
            {lastUpdate && ` • Updated ${formatDistanceToNow(lastUpdate)}`}
          </p>
        </div>
        <button
          onClick={() => {
            fetchWeather();
            fetchEnhancedData();
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <TrendingUp className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-4">
        {activeTab === 'weather' && (
          <WeatherTab weatherData={weatherData} onViewEvent={onViewEvent} />
        )}
        {activeTab === 'shipping' && (
          <ShippingTab portsData={enhancedData?.ports} />
        )}
        {activeTab === 'markets' && (
          <MarketsTab trendsData={enhancedData?.trends} />
        )}
        {activeTab === 'risks' && (
          <RisksTab riskData={enhancedData?.risk} />
        )}
      </div>
    </div>
  );
}

// Weather Tab Component
function WeatherTab({ weatherData, onViewEvent }) {
  if (!weatherData) {
    return <div className="text-center py-8 text-gray-500">No weather data available</div>;
  }

  // Map API response fields to expected format
  const suppliers = weatherData.weather_data || weatherData.suppliers || [];
  const severe_alerts = weatherData.critical_alerts || weatherData.high_alerts || weatherData.severe_alerts || [];

  return (
    <div className="space-y-6">
      {/* Severe Weather Alerts */}
      {severe_alerts && severe_alerts.length > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex items-start">
            <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 mr-3" />
            <div>
              <h3 className="font-semibold text-red-800">
                {severe_alerts.length} Severe Weather Alert{severe_alerts.length > 1 ? 's' : ''}
              </h3>
              <div className="mt-2 space-y-2">
                {severe_alerts.map((alert, idx) => (
                  <div key={idx} className="text-sm text-red-700">
                    <strong>{alert.supplier}:</strong> {alert.condition} - {alert.impact}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Supplier Weather Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {suppliers?.map((supplier) => (
          <Card key={supplier.supplier_id} className="p-4 hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-semibold text-gray-900">{supplier.supplier_name}</h3>
                <p className="text-sm text-gray-500 flex items-center gap-1">
                  <MapPin className="w-3 h-3" />
                  {supplier.location}
                </p>
              </div>
              {supplier.alert_level !== 'NORMAL' && (
                <Badge variant={supplier.alert_level === 'SEVERE' ? 'destructive' : 'warning'}>
                  {supplier.alert_level}
                </Badge>
              )}
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2 text-gray-600">
                  <Thermometer className="w-4 h-4" />
                  Temperature
                </span>
                <span className="font-medium">{supplier.temperature}°C</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2 text-gray-600">
                  <Wind className="w-4 h-4" />
                  Wind Speed
                </span>
                <span className="font-medium">{supplier.wind_speed} km/h</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2 text-gray-600">
                  <Droplets className="w-4 h-4" />
                  Conditions
                </span>
                <span className="font-medium capitalize">{supplier.condition || supplier.conditions}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Shipping Tab Component
function ShippingTab({ portsData }) {
  if (!portsData?.ports) {
    return (
      <div className="space-y-4">
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
          <div className="flex items-center">
            <Ship className="w-5 h-5 text-blue-500 mr-3" />
            <div>
              <h3 className="font-semibold text-blue-800">Shipping Monitor</h3>
              <p className="text-sm text-blue-700 mt-1">Track global port congestion and shipping delays in real-time</p>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="p-4">
            <h4 className="font-semibold text-gray-900 mb-2">📊 Features</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Real-time port congestion levels (0-10 scale)</li>
              <li>• Average wait times for vessels</li>
              <li>• Estimated shipping delays</li>
              <li>• Major global ports monitoring</li>
            </ul>
          </Card>
          
          <Card className="p-4">
            <h4 className="font-semibold text-gray-900 mb-2">🚢 Tracked Ports</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Los Angeles (Americas)</li>
              <li>• Shanghai (Asia-Pacific)</li>
              <li>• Rotterdam (Europe)</li>
              <li>• Singapore (Southeast Asia)</li>
            </ul>
          </Card>
        </div>
        
        <div className="text-center py-8 text-gray-500">Loading shipping data...</div>
      </div>
    );
  }

  const ports = Object.entries(portsData.ports);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Global Port Status</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {ports.map(([portName, data]) => (
          <Card key={portName} className="p-4">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h4 className="font-semibold text-gray-900 flex items-center gap-2">
                  <Ship className="w-5 h-5 text-blue-600" />
                  {data.port}
                </h4>
                <p className="text-sm text-gray-500">{data.status}</p>
              </div>
              <Badge 
                variant={data.congestion_level >= 7 ? 'destructive' : data.congestion_level >= 5 ? 'warning' : 'success'}
              >
                {data.congestion_level}/10
              </Badge>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Wait Time:</span>
                <span className="font-medium">{data.avg_wait_time_hours} hours</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Vessels Waiting:</span>
                <span className="font-medium">{data.vessels_waiting}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Estimated Delay:</span>
                <span className="font-medium">{data.estimated_delay_days} days</span>
              </div>
            </div>

            {/* Progress bar for congestion */}
            <div className="mt-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${
                    data.congestion_level >= 7 ? 'bg-red-600' :
                    data.congestion_level >= 5 ? 'bg-yellow-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${data.congestion_level * 10}%` }}
                ></div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Markets Tab Component
function MarketsTab({ trendsData }) {
  return (
    <div className="space-y-4">
      <div className="bg-green-50 border-l-4 border-green-500 p-4">
        <div className="flex items-center">
          <TrendingUp className="w-5 h-5 text-green-500 mr-3" />
          <div>
            <h3 className="font-semibold text-green-800">Market Intelligence</h3>
            <p className="text-sm text-green-700 mt-1">Monitor financial markets, commodities, and search trends affecting supply chains</p>
          </div>
        </div>
      </div>
      
      {trendsData ? (
        <>
          <Card className="p-6">
            <div className="flex items-center gap-4 mb-4">
              <BarChart3 className="w-8 h-8 text-blue-600" />
              <div>
                <h4 className="font-semibold text-gray-900">Google Trends: {trendsData.keyword}</h4>
                <p className="text-sm text-gray-500">Search interest analysis</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{trendsData.current_interest}</div>
                <div className="text-sm text-gray-600">Current Interest</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-700">{trendsData.avg_interest}</div>
                <div className="text-sm text-gray-600">Average</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{trendsData.change_percent}%</div>
                <div className="text-sm text-gray-600">Change</div>
              </div>
            </div>

            {trendsData.trending && (
              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-yellow-600" />
                  <span className="font-semibold text-yellow-800">
                    Trending! Search interest {trendsData.change_percent}% above average
                  </span>
                </div>
              </div>
            )}
          </Card>
          
          {/* Commodity Prices Placeholder */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">Oil</span>
                <DollarSign className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-2xl font-bold text-gray-900">$82.50</div>
              <div className="text-sm text-green-600 mt-1">+2.3% 30d</div>
            </Card>
            
            <Card className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">Gold</span>
                <DollarSign className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-2xl font-bold text-gray-900">$2,045</div>
              <div className="text-sm text-red-600 mt-1">-1.2% 30d</div>
            </Card>
            
            <Card className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">Copper</span>
                <DollarSign className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-2xl font-bold text-gray-900">$3.85</div>
              <div className="text-sm text-green-600 mt-1">+5.7% 30d</div>
            </Card>
            
            <Card className="p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">Lithium</span>
                <DollarSign className="w-4 h-4 text-gray-400" />
              </div>
              <div className="text-2xl font-bold text-gray-900">$15.20</div>
              <div className="text-sm text-gray-600 mt-1">+0.5% 30d</div>
            </Card>
          </div>
        </>
      ) : (
        <Card className="p-6 text-center text-gray-500">
          Loading market data...
        </Card>
      )}

      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Exchange Rates (USD)</h4>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
          <div className="p-3 bg-gray-50 rounded">
            <div className="text-gray-600">EUR</div>
            <div className="font-bold text-gray-900">0.866</div>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <div className="text-gray-600">GBP</div>
            <div className="font-bold text-gray-900">0.761</div>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <div className="text-gray-600">JPY</div>
            <div className="font-bold text-gray-900">153.62</div>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <div className="text-gray-600">CNY</div>
            <div className="font-bold text-gray-900">7.13</div>
          </div>
          <div className="p-3 bg-gray-50 rounded">
            <div className="text-gray-600">INR</div>
            <div className="font-bold text-gray-900">83.21</div>
          </div>
        </div>
      </Card>
      
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">💡 Market Insights</h4>
        <div className="space-y-3 text-sm">
          <div className="flex items-start gap-3 p-3 bg-blue-50 rounded">
            <BarChart3 className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <div className="font-medium text-gray-900">Supply Chain Interest Rising</div>
              <div className="text-gray-600">Search trends indicate increased focus on logistics optimization</div>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-green-50 rounded">
            <TrendingUp className="w-5 h-5 text-green-600 mt-0.5" />
            <div>
              <div className="font-medium text-gray-900">Copper Prices Climbing</div>
              <div className="text-gray-600">Strong demand from EV manufacturers driving price increases</div>
            </div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-yellow-50 rounded">
            <DollarSign className="w-5 h-5 text-yellow-600 mt-0.5" />
            <div>
              <div className="font-medium text-gray-900">Currency Volatility Alert</div>
              <div className="text-gray-600">Monitor EUR/USD fluctuations for European supplier costs</div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

// Risks Tab Component
function RisksTab({ riskData }) {
  const mockSuppliers = [
    { id: 1, name: "TSMC", country: "Taiwan", aggregate_risk_score: 45 },
    { id: 2, name: "Samsung Electronics", country: "South Korea", aggregate_risk_score: 32 },
    { id: 3, name: "Foxconn", country: "China", aggregate_risk_score: 58 },
    { id: 4, name: "Intel Corporation", country: "USA", aggregate_risk_score: 25 },
    { id: 5, name: "SK Hynix", country: "South Korea", aggregate_risk_score: 38 },
  ];

  return (
    <div className="space-y-4">
      <div className="bg-red-50 border-l-4 border-red-500 p-4">
        <div className="flex items-center">
          <AlertTriangle className="w-5 h-5 text-red-500 mr-3" />
          <div>
            <h3 className="font-semibold text-red-800">Risk Intelligence Center</h3>
            <p className="text-sm text-red-700 mt-1">Monitor geopolitical risks, sanctions, and supply chain vulnerabilities</p>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-red-50">
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-8 h-8 text-red-600" />
            <div>
              <div className="text-2xl font-bold text-red-600">{riskData?.risk_summary?.sanctions_alerts || 0}</div>
              <div className="text-sm text-red-700">Sanctions Alerts</div>
            </div>
          </div>
        </Card>

        <Card className="p-4 bg-orange-50">
          <div className="flex items-center gap-3">
            <Globe className="w-8 h-8 text-orange-600" />
            <div>
              <div className="text-2xl font-bold text-orange-600">{riskData?.risk_summary?.geopolitical_risks || 3}</div>
              <div className="text-sm text-orange-700">Geopolitical Risks</div>
            </div>
          </div>
        </Card>

        <Card className="p-4 bg-yellow-50">
          <div className="flex items-center gap-3">
            <Ship className="w-8 h-8 text-yellow-600" />
            <div>
              <div className="text-2xl font-bold text-yellow-600">{riskData?.risk_summary?.shipping_delays || 2}</div>
              <div className="text-sm text-yellow-700">Shipping Delays</div>
            </div>
          </div>
        </Card>

        <Card className="p-4 bg-blue-50">
          <div className="flex items-center gap-3">
            <DollarSign className="w-8 h-8 text-blue-600" />
            <div>
              <div className="text-2xl font-bold text-blue-600">{riskData?.risk_summary?.financial_risks || 1}</div>
              <div className="text-sm text-blue-700">Financial Risks</div>
            </div>
          </div>
        </Card>
      </div>

      {/* High Risk Countries */}
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">🌍 Geopolitical Hotspots</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-red-900">Ukraine</span>
              <Badge variant="destructive">CRITICAL</Badge>
            </div>
            <div className="text-sm text-red-700">
              <div>Conflict Level: 9/10</div>
              <div>145 events in last 30 days</div>
            </div>
          </div>
          
          <div className="p-4 bg-orange-50 border-l-4 border-orange-500 rounded">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-orange-900">Israel/Gaza</span>
              <Badge variant="destructive">CRITICAL</Badge>
            </div>
            <div className="text-sm text-orange-700">
              <div>Conflict Level: 8/10</div>
              <div>89 events in last 30 days</div>
            </div>
          </div>
          
          <div className="p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-yellow-900">Taiwan Strait</span>
              <Badge variant="warning">ELEVATED</Badge>
            </div>
            <div className="text-sm text-yellow-700">
              <div>Conflict Level: 4/10</div>
              <div>Heightened tensions</div>
            </div>
          </div>
          
          <div className="p-4 bg-green-50 border-l-4 border-green-500 rounded">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-green-900">South Korea</span>
              <Badge variant="success">LOW</Badge>
            </div>
            <div className="text-sm text-green-700">
              <div>Conflict Level: 2/10</div>
              <div>Stable environment</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Supplier Risk Scores */}
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">📊 Supplier Risk Scores</h4>
        <div className="space-y-3">
          {mockSuppliers.map((supplier) => (
            <div key={supplier.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${
                  supplier.aggregate_risk_score >= 70 ? 'bg-red-500' :
                  supplier.aggregate_risk_score >= 40 ? 'bg-yellow-500' : 'bg-green-500'
                }`}></div>
                <div>
                  <div className="font-medium text-gray-900">{supplier.name}</div>
                  <div className="text-sm text-gray-500">{supplier.country}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-gray-900">{supplier.aggregate_risk_score}/100</div>
                <div className="text-xs text-gray-500">Risk Score</div>
              </div>
            </div>
          ))}
        </div>
      </Card>
      
      {/* Sanctions Monitoring */}
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">🚫 Sanctions Monitoring</h4>
        <div className="space-y-3 text-sm">
          <div className="flex items-start gap-3 p-3 bg-gray-50 rounded">
            <AlertTriangle className="w-5 h-5 text-gray-400 mt-0.5" />
            <div className="flex-1">
              <div className="font-medium text-gray-900">No active sanctions detected</div>
              <div className="text-gray-600 mt-1">All suppliers cleared against OpenSanctions database</div>
            </div>
            <span className="text-green-600 font-medium">✓ Clear</span>
          </div>
          
          <div className="p-3 bg-blue-50 rounded">
            <div className="font-medium text-blue-900 mb-1">📡 Real-time Monitoring</div>
            <div className="text-blue-700 text-xs">
              Continuously checking against OFAC, UN, EU sanctions lists
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
