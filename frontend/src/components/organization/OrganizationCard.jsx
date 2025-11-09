import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, MapPin, TrendingUp, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Badge from '../ui/Badge';
import { getRiskScoreColor, formatRiskScore } from '../../utils/riskUtils';

const OrganizationCard = ({ organization }) => {
  const navigate = useNavigate();

  const getRiskLevel = (score) => {
    if (score >= 80) return { level: 'CRITICAL', color: 'destructive' };
    if (score >= 60) return { level: 'HIGH', color: 'destructive' };
    if (score >= 40) return { level: 'MEDIUM', color: 'default' };
    if (score >= 20) return { level: 'LOW', color: 'secondary' };
    return { level: 'MINIMAL', color: 'secondary' };
  };

  const riskInfo = getRiskLevel(organization.current_risk_score);

  return (
    <Card 
      className="hover:shadow-lg transition-shadow cursor-pointer"
      onClick={() => navigate(`/organization/${organization.id}`)}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Building2 className="h-6 w-6 text-primary" />
            </div>
            <div>
              <CardTitle className="text-xl">{organization.name}</CardTitle>
              <div className="flex items-center text-sm text-muted-foreground mt-1">
                <MapPin className="h-3 w-3 mr-1" />
                {organization.headquarters_location}
              </div>
            </div>
          </div>
          <Badge variant={riskInfo.color}>
            {riskInfo.level}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Industry</span>
            <span className="font-medium">{organization.industry}</span>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Risk Score</span>
            <div className="flex items-center space-x-2">
              <TrendingUp className={`h-4 w-4 ${getRiskScoreColor(organization.current_risk_score)}`} />
              <span className={`font-bold text-lg ${getRiskScoreColor(organization.current_risk_score)}`}>
                {formatRiskScore(organization.current_risk_score)}
              </span>
              <span className="text-muted-foreground">/100</span>
            </div>
          </div>

          {organization.description && (
            <p className="text-sm text-muted-foreground line-clamp-2 mt-3">
              {organization.description}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default OrganizationCard;