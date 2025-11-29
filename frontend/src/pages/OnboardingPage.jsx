import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Ship, MapPin, Building2, ArrowRight, ArrowLeft, AlertTriangle, Plus, X, Factory } from 'lucide-react';
import { organizationsAPI } from '../services/api';
import Button from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Alert, { AlertTitle, AlertDescription } from '../components/ui/Alert';
import Spinner from '../components/ui/Spinner';

const OnboardingPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [historicalEvents, setHistoricalEvents] = useState([]);
  const [weatherData, setWeatherData] = useState([]);
  
  const [formData, setFormData] = useState({
    // Step 1: Company Info
    companyName: '',
    industry: 'Electronics',
    headquarters: '',
    description: '',
    
    // Step 2: Shipping Route
    originPort: '',
    originCountry: '',
    originLatitude: '',
    originLongitude: '',
    destinationPort: '',
    destinationCountry: '',
    destinationLatitude: '',
    destinationLongitude: '',
    
    // Step 3: Supplier Locations
    suppliers: []
  });

  const industries = [
    'Electronics',
    'Pharmaceutical',
    'Automotive',
    'Food & Beverage',
    'Other'
  ];

  const commonRoutes = [
    {
      name: 'Singapore → Los Angeles',
      origin: { port: 'Port of Singapore', country: 'Singapore', lat: 1.2644, lon: 103.8215 },
      destination: { port: 'Port of Los Angeles', country: 'USA', lat: 33.7405, lon: -118.2716 }
    },
    {
      name: 'Shanghai → Rotterdam',
      origin: { port: 'Port of Shanghai', country: 'China', lat: 31.2304, lon: 121.4737 },
      destination: { port: 'Port of Rotterdam', country: 'Netherlands', lat: 51.9244, lon: 4.4777 }
    },
    {
      name: 'Hong Kong → Long Beach',
      origin: { port: 'Port of Hong Kong', country: 'Hong Kong', lat: 22.3193, lon: 114.1694 },
      destination: { port: 'Port of Long Beach', country: 'USA', lat: 33.7546, lon: -118.1995 }
    }
  ];

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const selectRoute = (route) => {
    setFormData({
      ...formData,
      originPort: route.origin.port,
      originCountry: route.origin.country,
      originLatitude: route.origin.lat.toString(),
      originLongitude: route.origin.lon.toString(),
      destinationPort: route.destination.port,
      destinationCountry: route.destination.country,
      destinationLatitude: route.destination.lat.toString(),
      destinationLongitude: route.destination.lon.toString(),
    });
  };

  const addSupplier = () => {
    setFormData({
      ...formData,
      suppliers: [...formData.suppliers, { name: '', city: '', country: '', latitude: '', longitude: '' }]
    });
  };

  const removeSupplier = (index) => {
    setFormData({
      ...formData,
      suppliers: formData.suppliers.filter((_, i) => i !== index)
    });
  };

  const updateSupplier = (index, field, value) => {
    const updatedSuppliers = [...formData.suppliers];
    updatedSuppliers[index][field] = value;
    setFormData({ ...formData, suppliers: updatedSuppliers });
  };

  const fetchHistoricalEvents = async () => {
    setLoading(true);
    try {
      // Call backend API to get historical events for the shipping route
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/events/historical`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin_latitude: parseFloat(formData.originLatitude),
          origin_longitude: parseFloat(formData.originLongitude),
          destination_latitude: parseFloat(formData.destinationLatitude),
          destination_longitude: parseFloat(formData.destinationLongitude),
          radius_km: 500
        })
      });
      
      const data = await response.json();
      setHistoricalEvents(data.events || []);
    } catch (error) {
      console.error('Failed to fetch historical events:', error);
      setHistoricalEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchSupplierMonitoring = async () => {
    if (formData.suppliers.length === 0) {
      setWeatherData([]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/monitoring/historical`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          suppliers: formData.suppliers.map(s => ({
            name: s.name,
            city: s.city,
            country: s.country,
            latitude: parseFloat(s.latitude),
            longitude: parseFloat(s.longitude)
          }))
        })
      });

      const data = await response.json();
      setWeatherData(data.monitoring_data || []);
    } catch (error) {
      console.error('Failed to fetch supplier monitoring data:', error);
      setWeatherData([]);
    } finally {
      setLoading(false);
    }
  };

  const createOrganizationMutation = useMutation({
    mutationFn: async (data) => {
      const response = await organizationsAPI.create(data);
      return response.data;
    },
    onSuccess: (org) => {
      queryClient.invalidateQueries(['organizations']);
      navigate('/');
    }
  });

  const handleNext = (e) => {
    if (e) e.preventDefault();
    if (step === 2) {
      // Fetch historical events when moving from Step 2 (Shipping Route) to Step 3 (Suppliers)
      fetchHistoricalEvents();
    }
    if (step === 3) {
      // Fetch supplier monitoring data when moving from Step 3 (Suppliers) to Step 4 (Historical Analysis)
      fetchSupplierMonitoring();
    }
    setStep(step + 1);
  };

  const handleBack = (e) => {
    if (e) e.preventDefault();
    setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    await createOrganizationMutation.mutateAsync({
      name: formData.companyName,
      industry: formData.industry,
      headquarters_location: formData.headquarters,
      description: formData.description,
      shipping_route: {
        origin: {
          port: formData.originPort,
          country: formData.originCountry,
          latitude: parseFloat(formData.originLatitude),
          longitude: parseFloat(formData.originLongitude)
        },
        destination: {
          port: formData.destinationPort,
          country: formData.destinationCountry,
          latitude: parseFloat(formData.destinationLatitude),
          longitude: parseFloat(formData.destinationLongitude)
        }
      }
    });
  };

  const isStep1Valid = formData.companyName && formData.industry && formData.headquarters;
  const isStep2Valid = formData.originPort && formData.destinationPort;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {[1, 2, 3, 4].map((s) => (
              <div key={s} className="flex items-center flex-1">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
                  step >= s ? 'bg-primary text-white' : 'bg-gray-300 text-gray-600'
                }`}>
                  {s}
                </div>
                {s < 4 && (
                  <div className={`flex-1 h-1 mx-2 ${
                    step > s ? 'bg-primary' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-2 text-sm">
            <span className={step >= 1 ? 'text-primary font-medium' : 'text-gray-500'}>Company Info</span>
            <span className={step >= 2 ? 'text-primary font-medium' : 'text-gray-500'}>Shipping Route</span>
            <span className={step >= 3 ? 'text-primary font-medium' : 'text-gray-500'}>Supplier Locations</span>
            <span className={step >= 4 ? 'text-primary font-medium' : 'text-gray-500'}>Historical Analysis</span>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>
              {step === 1 && <><Building2 className="inline mr-2" />Company Information</>}
              {step === 2 && <><Ship className="inline mr-2" />Shipping Route</>}
              {step === 3 && <><Factory className="inline mr-2" />Supplier Locations</>}
              {step === 4 && <><AlertTriangle className="inline mr-2" />Historical Risk Analysis</>}
            </CardTitle>
            <CardDescription>
              {step === 1 && 'Tell us about your company'}
              {step === 2 && 'Define your primary shipping route'}
              {step === 3 && 'Add your critical supplier locations'}
              {step === 4 && 'Review past events along your route and supplier regions'}
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Step 1: Company Info */}
            {step === 1 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Company Name *</label>
                  <Input
                    name="companyName"
                    value={formData.companyName}
                    onChange={handleInputChange}
                    placeholder="e.g., TechCore Electronics"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Industry *</label>
                  <select
                    name="industry"
                    value={formData.industry}
                    onChange={handleInputChange}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  >
                    {industries.map(ind => (
                      <option key={ind} value={ind}>{ind}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Headquarters Location *</label>
                  <Input
                    name="headquarters"
                    value={formData.headquarters}
                    onChange={handleInputChange}
                    placeholder="e.g., San Jose, California"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Description (Optional)</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Brief description of your business"
                    rows="3"
                    className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>
              </div>
            )}

            {/* Step 2: Shipping Route */}
            {step === 2 && (
              <div className="space-y-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm font-medium text-blue-900 mb-3">Quick Select Common Routes:</p>
                  <div className="space-y-2">
                    {commonRoutes.map((route, idx) => (
                      <button
                        key={idx}
                        onClick={() => selectRoute(route)}
                        className="w-full text-left px-4 py-3 bg-white hover:bg-blue-100 rounded-md border border-blue-200 transition-colors"
                      >
                        <div className="flex items-center">
                          <Ship className="h-4 w-4 mr-2 text-blue-600" />
                          <span className="font-medium">{route.name}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-4">
                    <h3 className="font-semibold text-lg flex items-center">
                      <MapPin className="h-5 w-5 mr-2 text-green-600" />
                      Origin
                    </h3>
                    <Input
                      name="originPort"
                      value={formData.originPort}
                      onChange={handleInputChange}
                      placeholder="Port Name *"
                      required
                    />
                    <Input
                      name="originCountry"
                      value={formData.originCountry}
                      onChange={handleInputChange}
                      placeholder="Country *"
                      required
                    />
                    <Input
                      name="originLatitude"
                      value={formData.originLatitude}
                      onChange={handleInputChange}
                      placeholder="Latitude *"
                      type="number"
                      step="any"
                      required
                    />
                    <Input
                      name="originLongitude"
                      value={formData.originLongitude}
                      onChange={handleInputChange}
                      placeholder="Longitude *"
                      type="number"
                      step="any"
                      required
                    />
                  </div>

                  <div className="space-y-4">
                    <h3 className="font-semibold text-lg flex items-center">
                      <MapPin className="h-5 w-5 mr-2 text-red-600" />
                      Destination
                    </h3>
                    <Input
                      name="destinationPort"
                      value={formData.destinationPort}
                      onChange={handleInputChange}
                      placeholder="Port Name *"
                      required
                    />
                    <Input
                      name="destinationCountry"
                      value={formData.destinationCountry}
                      onChange={handleInputChange}
                      placeholder="Country *"
                      required
                    />
                    <Input
                      name="destinationLatitude"
                      value={formData.destinationLatitude}
                      onChange={handleInputChange}
                      placeholder="Latitude *"
                      type="number"
                      step="any"
                      required
                    />
                    <Input
                      name="destinationLongitude"
                      value={formData.destinationLongitude}
                      onChange={handleInputChange}
                      placeholder="Longitude *"
                      type="number"
                      step="any"
                      required
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Supplier Locations */}
            {step === 3 && (
              <div className="space-y-4">
                <Alert>
                  <AlertTitle>Add Critical Supplier Locations</AlertTitle>
                  <AlertDescription>
                    Add the locations of your key suppliers. We'll show you historical weather patterns and 
                    supply chain events for these regions to help you assess location-specific risks.
                  </AlertDescription>
                </Alert>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm font-medium text-blue-900 mb-3">Common Supplier Locations:</p>
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      { name: 'Taiwan (Hsinchu)', city: 'Hsinchu', country: 'Taiwan', lat: '24.8138', lon: '120.9675' },
                      { name: 'China (Shenzhen)', city: 'Shenzhen', country: 'China', lat: '22.5431', lon: '114.0579' },
                      { name: 'Singapore', city: 'Singapore', country: 'Singapore', lat: '1.3521', lon: '103.8198' },
                      { name: 'South Korea (Seoul)', city: 'Seoul', country: 'South Korea', lat: '37.5665', lon: '126.978' }
                    ].map((template, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setFormData({
                          ...formData,
                          suppliers: [...formData.suppliers, {
                            name: template.name,
                            city: template.city,
                            country: template.country,
                            latitude: template.lat,
                            longitude: template.lon
                          }]
                        })}
                        className="text-sm px-3 py-2 bg-white hover:bg-blue-100 rounded border border-blue-200 transition-colors text-left"
                      >
                        + {template.name}
                      </button>
                    ))}
                  </div>
                </div>

                {formData.suppliers.length > 0 && (
                  <div className="space-y-3">
                    {formData.suppliers.map((supplier, idx) => (
                      <div key={idx} className="p-4 bg-white rounded-lg border border-gray-200">
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-medium flex items-center">
                            <Factory className="h-4 w-4 mr-2 text-blue-600" />
                            Supplier {idx + 1}
                          </h4>
                          <button
                            type="button"
                            onClick={() => removeSupplier(idx)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <X className="h-4 w-4" />
                          </button>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                          <Input
                            placeholder="Supplier Name"
                            value={supplier.name}
                            onChange={(e) => updateSupplier(idx, 'name', e.target.value)}
                          />
                          <Input
                            placeholder="City"
                            value={supplier.city}
                            onChange={(e) => updateSupplier(idx, 'city', e.target.value)}
                          />
                          <Input
                            placeholder="Country"
                            value={supplier.country}
                            onChange={(e) => updateSupplier(idx, 'country', e.target.value)}
                          />
                          <Input
                            placeholder="Latitude"
                            type="number"
                            step="any"
                            value={supplier.latitude}
                            onChange={(e) => updateSupplier(idx, 'latitude', e.target.value)}
                          />
                          <Input
                            placeholder="Longitude"
                            type="number"
                            step="any"
                            value={supplier.longitude}
                            onChange={(e) => updateSupplier(idx, 'longitude', e.target.value)}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                <Button
                  type="button"
                  onClick={addSupplier}
                  variant="outline"
                  className="w-full"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Add Custom Supplier Location
                </Button>

                {formData.suppliers.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Factory className="h-12 w-12 mx-auto mb-3 text-gray-400" />
                    <p>No suppliers added yet.</p>
                    <p className="text-sm mt-1">Add supplier locations to see location-specific risk analysis.</p>
                  </div>
                )}
              </div>
            )}

            {/* Step 4: Historical Events */}
            {step === 4 && (
              <div className="space-y-6">
                {loading ? (
                  <div className="flex items-center justify-center py-12">
                    <Spinner size="lg" />
                    <span className="ml-3 text-gray-600">Analyzing historical data...</span>
                  </div>
                ) : (
                  <>
                    {/* Shipping Route Events */}
                    <div>
                      <Alert>
                        <AlertTitle>📦 Shipping Route Risk Analysis</AlertTitle>
                        <AlertDescription>
                          Historical events along <strong>{formData.originPort}</strong> → <strong>{formData.destinationPort}</strong> (500km radius)
                        </AlertDescription>
                      </Alert>

                      {historicalEvents.length > 0 ? (
                        <div className="mt-3 space-y-3">
                          {historicalEvents.map((event, idx) => (
                            <div key={idx} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                              <h4 className="font-medium text-gray-900">{event.title}</h4>
                              <p className="text-sm text-gray-600 mt-1">{event.description}</p>
                              <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                                <span>📅 {event.date}</span>
                                <span>📍 {event.location}</span>
                                <span className={`px-2 py-1 rounded ${
                                  event.severity === 'High' ? 'bg-red-100 text-red-700' :
                                  event.severity === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                                  'bg-blue-100 text-blue-700'
                                }`}>
                                  {event.severity} Severity
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="mt-3 text-center py-6 text-gray-500 bg-gray-50 rounded-lg">
                          <p className="text-sm">No significant events found for this route.</p>
                        </div>
                      )}
                    </div>

                    {/* Supplier Location Monitoring */}
                    {weatherData.length > 0 && (
                      <div>
                        <Alert>
                          <AlertTitle>🏭 Supplier Location Analysis</AlertTitle>
                          <AlertDescription>
                            Historical weather patterns and events for your {weatherData.length} supplier location{weatherData.length > 1 ? 's' : ''} (last 30 days)
                          </AlertDescription>
                        </Alert>

                        <div className="mt-3 space-y-4">
                          {weatherData.map((data, idx) => (
                            <div key={idx} className="p-4 bg-white rounded-lg border border-gray-300">
                              <div className="flex items-start justify-between mb-3">
                                <div>
                                  <h4 className="font-medium text-gray-900 flex items-center">
                                    <Factory className="h-4 w-4 mr-2 text-blue-600" />
                                    {data.supplier.name || `${data.supplier.city}, ${data.supplier.country}`}
                                  </h4>
                                  <p className="text-xs text-gray-500 mt-1">
                                    📍 {data.supplier.city}, {data.supplier.country}
                                  </p>
                                </div>
                                <div className="text-right">
                                  <div className={`text-xs px-2 py-1 rounded ${
                                    data.risk_indicators.historical_disruptions > 2 ? 'bg-red-100 text-red-700' :
                                    data.risk_indicators.historical_disruptions > 0 ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-green-100 text-green-700'
                                  }`}>
                                    {data.risk_indicators.historical_disruptions} Event{data.risk_indicators.historical_disruptions !== 1 ? 's' : ''}
                                  </div>
                                </div>
                              </div>

                              {/* Weather Summary */}
                              <div className="grid grid-cols-3 gap-3 mb-3 text-sm">
                                <div className="bg-blue-50 p-2 rounded">
                                  <div className="text-xs text-gray-600">Avg Temp</div>
                                  <div className="font-medium">
                                    {data.weather_summary.avg_temp_min}°C - {data.weather_summary.avg_temp_max}°C
                                  </div>
                                </div>
                                <div className="bg-blue-50 p-2 rounded">
                                  <div className="text-xs text-gray-600">Precipitation</div>
                                  <div className="font-medium">{data.weather_summary.precipitation_days} days</div>
                                </div>
                                <div className="bg-blue-50 p-2 rounded">
                                  <div className="text-xs text-gray-600">Max Wind</div>
                                  <div className="font-medium">{data.weather_summary.max_wind_speed} km/h</div>
                                </div>
                              </div>

                              {/* Nearby Events */}
                              {data.nearby_events.length > 0 && (
                                <div className="mt-3 pt-3 border-t border-gray-200">
                                  <p className="text-xs font-medium text-gray-700 mb-2">Historical Disruptions:</p>
                                  {data.nearby_events.map((event, eventIdx) => (
                                    <div key={eventIdx} className="text-xs bg-gray-50 p-2 rounded mb-1">
                                      <div className="font-medium">{event.title} ({event.distance_km} km away)</div>
                                      <div className="text-gray-600">{event.date} - {event.description}</div>
                                    </div>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
                      <p className="text-sm text-green-800">
                        <strong>✓ Analysis Complete!</strong> We'll monitor your routes and supplier regions for real-time disruptions and alert you to potential risks.
                      </p>
                    </div>
                  </>
                )}
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between pt-6 border-t">
              {step > 1 && (
                <Button type="button" variant="outline" onClick={handleBack}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back
                </Button>
              )}
              
              <div className="ml-auto">
                {step < 4 ? (
                  <Button
                    type="button"
                    onClick={handleNext}
                    disabled={
                      (step === 1 && !isStep1Valid) ||
                      (step === 2 && !isStep2Valid)
                    }
                  >
                    Next
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </Button>
                ) : (
                  <Button
                    type="button"
                    onClick={handleSubmit}
                    disabled={createOrganizationMutation.isLoading || loading}
                  >
                    {createOrganizationMutation.isLoading ? (
                      <>
                        <Spinner size="sm" className="mr-2" />
                        Creating...
                      </>
                    ) : (
                      'Complete Onboarding'
                    )}
                  </Button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default OnboardingPage;
