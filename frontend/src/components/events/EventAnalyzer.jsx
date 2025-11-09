import React, { useState } from 'react';
import { AlertTriangle, Send, Loader2 } from 'lucide-react';
import Button from '../ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card';
import Alert, { AlertTitle, AlertDescription } from '../ui/Alert';

const EventAnalyzer = ({ organizationId, onAnalysisComplete }) => {
  const [eventInput, setEventInput] = useState('');
  const [severityLevel, setSeverityLevel] = useState(3);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  const severityLabels = {
    1: 'Minor',
    2: 'Low',
    3: 'Moderate',
    4: 'High',
    5: 'Critical'
  };

  const severityColors = {
    1: 'bg-blue-500',
    2: 'bg-green-500',
    3: 'bg-yellow-500',
    4: 'bg-orange-500',
    5: 'bg-red-500'
  };

  const exampleEvents = [
    "Major earthquake hits Taiwan, magnitude 7.5",
    "Port strike in Los Angeles affecting shipping operations",
    "Factory fire at semiconductor manufacturing plant in South Korea",
    "Hurricane approaching Miami, Category 4",
    "Trade sanctions imposed on Chinese lithium suppliers"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!eventInput.trim()) return;

    setIsAnalyzing(true);
    setError(null);

    try {
      await onAnalysisComplete({
        organization_id: organizationId,
        event_input: eventInput,
        severity_level: severityLevel
      });
    } catch (err) {
      setError(err.message || 'Failed to analyze event');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const loadExample = (example) => {
    setEventInput(example);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <AlertTriangle className="h-5 w-5 mr-2 text-orange-500" />
          Custom Event Analysis
        </CardTitle>
        <CardDescription>
          Describe a supply chain incident to analyze its impact on your suppliers
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Incident Description
            </label>
            <textarea
              value={eventInput}
              onChange={(e) => setEventInput(e.target.value)}
              placeholder="Describe the incident... e.g., 'Major earthquake in Taiwan affecting semiconductor production'"
              rows="4"
              className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              required
              disabled={isAnalyzing}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Severity Level: {severityLabels[severityLevel]}
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="1"
                max="5"
                value={severityLevel}
                onChange={(e) => setSeverityLevel(parseInt(e.target.value))}
                className="flex-1 h-2 rounded-lg appearance-none cursor-pointer"
                disabled={isAnalyzing}
              />
              <div className={`w-12 h-12 rounded-full ${severityColors[severityLevel]} flex items-center justify-center text-white font-bold`}>
                {severityLevel}
              </div>
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Minor</span>
              <span>Moderate</span>
              <span>Critical</span>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="flex justify-end">
            <Button
              type="submit"
              disabled={isAnalyzing || !eventInput.trim()}
              className="w-full sm:w-auto"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  Analyze Event
                </>
              )}
            </Button>
          </div>
        </form>

        <div className="mt-6 pt-6 border-t">
          <p className="text-sm font-medium text-gray-700 mb-3">
            Try these examples:
          </p>
          <div className="space-y-2">
            {exampleEvents.map((example, idx) => (
              <button
                key={idx}
                onClick={() => loadExample(example)}
                disabled={isAnalyzing}
                className="w-full text-left px-3 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EventAnalyzer;