import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Spinner from '../ui/Spinner';
import Badge from '../ui/Badge';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const EnhancedDataPanel = ({ organizationId }) => {
  const [activeApi, setActiveApi] = useState('trends');

  // Test endpoint - shows all APIs at once
  const { data, isLoading } = useQuery({
    queryKey: ['enhanced-test'],
    queryFn: async () => {
      const response = await axios.get(`${API_BASE_URL}/api/enhanced/test/all`);
      return response.data;
    },
    refetchInterval: 60000, // Refresh every minute
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Spinner />
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span>💹</span> Enhanced Risk Data - Live APIs
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            {/* Financial Data */}
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-sm text-gray-600 mb-2">Financial</h3>
              {data?.tests?.stock_data && (
                <div className="space-y-1">
                  <p className="text-lg font-bold">{data.tests.stock_data.ticker}</p>
                  <p className="text-sm">${data.tests.stock_data.current_price}</p>
                  <Badge variant={data.tests.stock_data.price_change_5d > 0 ? 'success' : 'destructive'}>
                    {data.tests.stock_data.price_change_5d}%
                  </Badge>
                </div>
              )}
            </div>

            {/* Shipping Data */}
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-sm text-gray-600 mb-2">Shipping</h3>
              {data?.tests?.port_status && (
                <div className="space-y-1">
                  <p className="text-lg font-bold">{data.tests.port_status.port}</p>
                  <p className="text-sm">Congestion: {data.tests.port_status.congestion_level}/10</p>
                  <Badge variant={data.tests.port_status.congestion_level >= 7 ? 'destructive' : 'default'}>
                    {data.tests.port_status.status.split(' - ')[0]}
                  </Badge>
                </div>
              )}
            </div>

            {/* Geopolitical Data */}
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-sm text-gray-600 mb-2">Geopolitical</h3>
              {data?.tests?.conflict && (
                <div className="space-y-1">
                  <p className="text-lg font-bold">{data.tests.conflict.country}</p>
                  <p className="text-sm">Risk: {data.tests.conflict.conflict_level}/10</p>
                  <Badge variant={data.tests.conflict.conflict_level >= 7 ? 'destructive' : 'default'}>
                    {data.tests.conflict.status}
                  </Badge>
                </div>
              )}
            </div>

            {/* Exchange Rates */}
            <div className="p-4 border rounded-lg">
              <h3 className="font-semibold text-sm text-gray-600 mb-2">💱 Exchange Rates</h3>
              {data?.tests?.exchange_rates?.rates && (
                <div className="space-y-1 text-sm">
                  <p>EUR: {data.tests.exchange_rates.rates.EUR?.toFixed(4)}</p>
                  <p>GBP: {data.tests.exchange_rates.rates.GBP?.toFixed(4)}</p>
                  <p>JPY: {data.tests.exchange_rates.rates.JPY?.toFixed(2)}</p>
                </div>
              )}
            </div>

          </div>

          <div className="mt-4 text-sm text-gray-500 text-center">
            Data refreshes every minute • Last updated: {new Date(data?.timestamp).toLocaleTimeString()}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default EnhancedDataPanel;
