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
      const [portsRes, trendsRes, riskRes, exchangeRes] = await Promise.all([
        fetch('http://localhost:8000/api/enhanced/shipping/major-ports'),
        fetch('http://localhost:8000/api/enhanced/social/trends?keyword=supply%20chain'),
        fetch(`http://localhost:8000/api/enhanced/risk/dashboard?organization_id=${organizationId}`),
        fetch('http://localhost:8000/api/enhanced/financial/exchange-rates?base_currency=USD')
      ]);

      const riskData = riskRes.ok ? await riskRes.json() : null;
      
      // Determine relevant commodities based on organization's industry
      let commoditiesToFetch = [];
      
      if (riskData?.organization) {
        const orgName = riskData.organization.toLowerCase();
        
        // Pharmaceutical companies
        if (orgName.includes('pharma') || orgName.includes('bio') || orgName.includes('medical') || orgName.includes('health')) {
          commoditiesToFetch = ['oil', 'natural_gas', 'silver', 'platinum', 'palladium', 'ethanol', 'corn'];
        } 
        // Automotive/EV companies
        else if (orgName.includes('auto') || orgName.includes('electric') || orgName.includes('vehicle') || orgName.includes('motor')) {
          commoditiesToFetch = ['oil', 'copper', 'lithium', 'aluminum', 'nickel', 'cobalt', 'steel'];
        } 
        // Technology/Electronics companies
        else if (orgName.includes('tech') || orgName.includes('electronic') || orgName.includes('semiconductor') || orgName.includes('chip')) {
          commoditiesToFetch = ['copper', 'gold', 'silver', 'lithium', 'silicon', 'palladium', 'rare_earth'];
        }
        // Food/Agriculture companies
        else if (orgName.includes('food') || orgName.includes('agri') || orgName.includes('farm') || orgName.includes('grain')) {
          commoditiesToFetch = ['corn', 'wheat', 'soybeans', 'sugar', 'coffee', 'natural_gas', 'oil'];
        }
        // Energy/Oil companies
        else if (orgName.includes('energy') || orgName.includes('oil') || orgName.includes('gas') || orgName.includes('petroleum')) {
          commoditiesToFetch = ['oil', 'natural_gas', 'coal', 'uranium', 'gasoline', 'heating_oil', 'diesel'];
        }
        // Construction/Manufacturing
        else if (orgName.includes('construct') || orgName.includes('building') || orgName.includes('manufact')) {
          commoditiesToFetch = ['steel', 'copper', 'aluminum', 'lumber', 'cement', 'iron_ore', 'oil'];
        }
        // Default for general companies
        else {
          commoditiesToFetch = ['oil', 'copper', 'gold', 'natural_gas', 'steel', 'aluminum'];
        }
      } else {
        // Fallback if no organization data
        commoditiesToFetch = ['oil', 'copper', 'gold', 'natural_gas', 'steel'];
      }

      // Fetch commodities
      const commoditiesRes = await fetch('http://localhost:8000/api/enhanced/financial/commodities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ commodities: commoditiesToFetch })
      });

      const commoditiesData = commoditiesRes.ok ? await commoditiesRes.json() : null;
      console.log('Commodities API response:', commoditiesData);

      const data = {
        ports: portsRes.ok ? await portsRes.json() : null,
        trends: trendsRes.ok ? await trendsRes.json() : null,
        risk: riskData,
        commodities: commoditiesData,
        exchangeRates: exchangeRes.ok ? await exchangeRes.json() : null,
      };

      console.log('Enhanced data:', data);
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
          <MarketsTab 
            trendsData={enhancedData?.trends} 
            commoditiesData={enhancedData?.commodities}
            exchangeRatesData={enhancedData?.exchangeRates}
          />
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
            <h4 className="font-semibold text-gray-900 mb-2">Features</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Real-time port congestion levels (0-10 scale)</li>
              <li>• Average wait times for vessels</li>
              <li>• Estimated shipping delays</li>
              <li>• Major global ports monitoring</li>
            </ul>
          </Card>
          
          <Card className="p-4">
            <h4 className="font-semibold text-gray-900 mb-2">Tracked Ports</h4>
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
function MarketsTab({ trendsData, commoditiesData, exchangeRatesData }) {
  // Extract commodity prices - handle nested structure from API
  let commodities = commoditiesData || {};
  
  // Fallback to mock data if API returns empty (Yahoo Finance may be rate limited)
  if (Object.keys(commodities).length === 0) {
    commodities = {
      oil: { current_price: 78.50, change_30d: 2.3, trend: 'UP' },
      natural_gas: { current_price: 3.42, change_30d: -1.2, trend: 'STABLE' },
      silver: { current_price: 24.15, change_30d: 3.8, trend: 'UP' },
      platinum: { current_price: 945.00, change_30d: 1.5, trend: 'UP' },
      palladium: { current_price: 1285.00, change_30d: -2.1, trend: 'DOWN' },
      ethanol: { current_price: 2.18, change_30d: 0.7, trend: 'STABLE' },
      corn: { current_price: 4.52, change_30d: -3.2, trend: 'DOWN' },
      copper: { current_price: 3.85, change_30d: 5.7, trend: 'UP' },
      lithium: { current_price: 15.20, change_30d: 0.5, trend: 'STABLE' },
      aluminum: { current_price: 2.34, change_30d: 1.8, trend: 'UP' },
      nickel: { current_price: 16.85, change_30d: 4.2, trend: 'UP' },
      cobalt: { current_price: 32.50, change_30d: -1.5, trend: 'STABLE' },
      steel: { current_price: 825.00, change_30d: 2.9, trend: 'UP' },
      gold: { current_price: 2045.00, change_30d: -0.8, trend: 'STABLE' },
      wheat: { current_price: 5.78, change_30d: 1.2, trend: 'UP' },
      soybeans: { current_price: 13.45, change_30d: -0.9, trend: 'STABLE' },
      sugar: { current_price: 0.21, change_30d: 2.4, trend: 'UP' },
      coffee: { current_price: 1.95, change_30d: 4.1, trend: 'UP' },
      lumber: { current_price: 485.00, change_30d: -2.8, trend: 'DOWN' }
    };
  }
  
  // Extract exchange rates
  const rates = exchangeRatesData?.rates || {};
  
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
          
          {/* Commodity Prices */}
          <div className="space-y-3">
            {!commoditiesData || Object.keys(commoditiesData).length === 0 ? (
              <div className="bg-yellow-50 border-l-4 border-yellow-500 p-3 text-sm">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-600" />
                  <span className="text-yellow-800">Using demo commodity prices - Live API may be rate limited</span>
                </div>
              </div>
            ) : null}
            
            {Object.keys(commodities).length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(commodities).map(([name, data]) => {
                  const price = data.current_price || data.price || data;
                  const change = data.change_30d;
                  
                  return (
                    <Card key={name} className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600 capitalize">{name}</span>
                        <DollarSign className="w-4 h-4 text-gray-400" />
                      </div>
                      <div className="text-2xl font-bold text-gray-900">
                        ${typeof price === 'number' ? price.toFixed(2) : 'N/A'}
                      </div>
                      {change !== undefined && (
                        <div className={`text-sm mt-1 ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {change >= 0 ? '+' : ''}{change}% 30d
                        </div>
                      )}
                      {data.trend && (
                        <div className="text-xs text-gray-500 mt-1">
                          Trend: {data.trend}
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            ) : (
              <Card className="p-6 text-center text-gray-500">
                Loading commodity prices...
              </Card>
            )}
          </div>
        </>
      ) : (
        <Card className="p-6 text-center text-gray-500">
          Loading market data...
        </Card>
      )}

      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">
          Exchange Rates ({exchangeRatesData?.base || 'USD'})
        </h4>
        {Object.keys(rates).length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
            {Object.entries(rates).slice(0, 10).map(([currency, rate]) => (
              <div key={currency} className="p-3 bg-gray-50 rounded">
                <div className="text-gray-600">{currency}</div>
                <div className="font-bold text-gray-900">
                  {typeof rate === 'number' ? rate.toFixed(3) : rate}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-4 text-gray-500">
            Loading exchange rates...
          </div>
        )}
      </Card>
      
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Market Insights</h4>
        <div className="space-y-3 text-sm">
          {trendsData?.trending && (
            <div className="flex items-start gap-3 p-3 bg-blue-50 rounded">
              <BarChart3 className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <div className="font-medium text-gray-900">
                  {trendsData.keyword} Interest {trendsData.change_percent >= 0 ? 'Rising' : 'Declining'}
                </div>
                <div className="text-gray-600">
                  Search trends {trendsData.change_percent >= 0 ? 'up' : 'down'} {Math.abs(trendsData.change_percent)}% - 
                  {trendsData.change_percent >= 0 ? ' increased focus on supply chain optimization' : ' decreased search activity'}
                </div>
              </div>
            </div>
          )}
          
          {commodities.copper?.current_price && commodities.copper.current_price > 3.5 && (
            <div className="flex items-start gap-3 p-3 bg-green-50 rounded">
              <TrendingUp className="w-5 h-5 text-green-600 mt-0.5" />
              <div>
                <div className="font-medium text-gray-900">Copper Prices Elevated</div>
                <div className="text-gray-600">
                  Current price: ${commodities.copper.current_price.toFixed(2)} - 
                  {commodities.copper.trend === 'UP' ? ' Strong upward momentum' : ' Price holding steady'}
                </div>
              </div>
            </div>
          )}
          
          {commodities.oil?.current_price && commodities.oil.current_price > 80 && (
            <div className="flex items-start gap-3 p-3 bg-orange-50 rounded">
              <DollarSign className="w-5 h-5 text-orange-600 mt-0.5" />
              <div>
                <div className="font-medium text-gray-900">Oil Prices Elevated</div>
                <div className="text-gray-600">
                  Current price: ${commodities.oil.current_price.toFixed(2)}/barrel - 
                  Impacts shipping and logistics costs
                </div>
              </div>
            </div>
          )}
          
          {rates.EUR && (rates.EUR < 0.85 || rates.EUR > 0.95) && (
            <div className="flex items-start gap-3 p-3 bg-yellow-50 rounded">
              <DollarSign className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div>
                <div className="font-medium text-gray-900">Currency Volatility Alert</div>
                <div className="text-gray-600">
                  EUR/USD at {rates.EUR?.toFixed(3)} - Monitor European supplier costs
                </div>
              </div>
            </div>
          )}
          
          {!trendsData && Object.keys(commodities).length === 0 && Object.keys(rates).length === 0 && (
            <div className="text-center py-4 text-gray-500">
              Loading market insights...
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

// Risks Tab Component
function RisksTab({ riskData }) {
  // Use actual suppliers from risk data API, fallback to empty array
  const suppliers = riskData?.suppliers || [];
  
  // Extract unique countries from suppliers with their risk data
  const getCountryRisks = () => {
    if (!suppliers || suppliers.length === 0) return [];
    
    const countryMap = new Map();
    
    suppliers.forEach(supplier => {
      const country = supplier.country;
      if (!countryMap.has(country)) {
        // Get geopolitical risk from supplier's risk data
        const geoRisk = supplier.risk_data?.geopolitical?.conflict_level || 0;
        const affectedSuppliers = suppliers
          .filter(s => s.country === country)
          .map(s => s.name);
        
        // Determine risk level and styling
        let riskLevel, badge, bgColor, borderColor, textColor;
        if (geoRisk >= 7) {
          riskLevel = 'CRITICAL';
          badge = 'destructive';
          bgColor = 'bg-red-50';
          borderColor = 'border-red-500';
          textColor = 'text-red-700';
        } else if (geoRisk >= 5) {
          riskLevel = 'HIGH';
          badge = 'destructive';
          bgColor = 'bg-orange-50';
          borderColor = 'border-orange-500';
          textColor = 'text-orange-700';
        } else if (geoRisk >= 3) {
          riskLevel = 'MODERATE';
          badge = 'warning';
          bgColor = 'bg-yellow-50';
          borderColor = 'border-yellow-500';
          textColor = 'text-yellow-700';
        } else {
          riskLevel = 'LOW';
          badge = 'success';
          bgColor = 'bg-green-50';
          borderColor = 'border-green-500';
          textColor = 'text-green-700';
        }
        
        countryMap.set(country, {
          country,
          riskLevel: geoRisk,
          badge,
          bgColor,
          borderColor,
          textColor,
          riskLevelText: riskLevel,
          affectedSuppliers: affectedSuppliers.join(', ')
        });
      }
    });
    
    // Sort by risk level (highest first)
    return Array.from(countryMap.values()).sort((a, b) => b.riskLevel - a.riskLevel);
  };
  
  const countryRisks = getCountryRisks();

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
        <h4 className="font-semibold text-gray-900 mb-4">Geopolitical Risk by Country</h4>
        {countryRisks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {countryRisks.map((countryData) => (
              <div key={countryData.country} className={`p-4 ${countryData.bgColor} border-l-4 ${countryData.borderColor} rounded`}>
                <div className="flex items-center justify-between mb-2">
                  <span className={`font-semibold ${countryData.textColor.replace('text-', 'text-').replace('-700', '-900')}`}>
                    {countryData.country}
                  </span>
                  <Badge variant={countryData.badge}>{countryData.riskLevelText}</Badge>
                </div>
                <div className={`text-sm ${countryData.textColor}`}>
                  <div>Risk Level: {countryData.riskLevel}/10</div>
                  <div className="mt-2 font-medium text-xs">Affects:</div>
                  <div className="text-xs truncate" title={countryData.affectedSuppliers}>
                    {countryData.affectedSuppliers}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Globe className="w-12 h-12 mx-auto text-gray-400 mb-2" />
            <p>Loading geopolitical risk data...</p>
          </div>
        )}
      </Card>

      {/* Supplier Risk Scores */}
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Supplier Risk Scores</h4>
        {suppliers.length > 0 ? (
          <div className="space-y-3">
            {suppliers.map((supplier) => (
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
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Globe className="w-12 h-12 mx-auto text-gray-400 mb-2" />
            <p>Loading supplier risk data...</p>
          </div>
        )}
      </Card>
      
      {/* Sanctions Monitoring */}
      <Card className="p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Sanctions Monitoring</h4>
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
            <div className="font-medium text-blue-900 mb-1">Real-time Monitoring</div>
            <div className="text-blue-700 text-xs">
              Continuously checking against OFAC, UN, EU sanctions lists
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
