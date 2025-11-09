import React from 'react';
import { MapPin, Package, Clock, TrendingUp } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';
import Badge from '../ui/Badge';
import { getCriticalityColor } from '../../utils/riskUtils';

const SupplierCard = ({ supplier }) => {
  const getTierBadge = (tier) => {
    const colors = {
      1: 'bg-purple-100 text-purple-800',
      2: 'bg-blue-100 text-blue-800',
      3: 'bg-gray-100 text-gray-800',
    };
    return colors[tier] || colors[1];
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="font-semibold text-lg text-gray-900">
              {supplier.name}
            </h3>
            <div className="flex items-center text-sm text-muted-foreground mt-1">
              <MapPin className="h-3 w-3 mr-1" />
              {supplier.city && `${supplier.city}, `}{supplier.country}
            </div>
          </div>
          
          <div 
            className={`w-3 h-3 rounded-full ${getCriticalityColor(supplier.criticality)}`}
            title={`${supplier.criticality} criticality`}
          />
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground flex items-center">
              <Package className="h-3 w-3 mr-1" />
              Category
            </span>
            <span className="font-medium">{supplier.category}</span>
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Tier</span>
            <Badge className={getTierBadge(supplier.tier)}>
              Tier {supplier.tier}
            </Badge>
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground flex items-center">
              <Clock className="h-3 w-3 mr-1" />
              Lead Time
            </span>
            <span className="font-medium">{supplier.lead_time_days} days</span>
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              Reliability
            </span>
            <span className="font-medium">{supplier.reliability_score}%</span>
          </div>

          <div className="pt-2 border-t">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Capacity</span>
              <div className="flex items-center space-x-2">
                <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary"
                    style={{ width: `${supplier.capacity_utilization}%` }}
                  />
                </div>
                <span className="font-medium text-xs">
                  {supplier.capacity_utilization}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SupplierCard;