import React, { useEffect } from 'react';
import { AlertTriangle, TrendingUp, Users, DollarSign } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Badge from '../ui/Badge';
import { getRiskLevelColor, formatRiskScore, getRiskScoreColor } from '../../utils/riskUtils';
import { formatCurrency } from '../../utils/formatters';

const RiskAssessmentDisplay = ({ riskAnalysis, affectedSuppliers, onRender }) => {
  if (!riskAnalysis) return null;

  const { 
    overall_risk_score, 
    risk_level, 
    key_metrics, 
    financial_impact,
    risk_summary 
  } = riskAnalysis;

  // Notify parent when component is rendered
  useEffect(() => {
    if (onRender) {
      onRender();
    }
  }, [onRender]);

  return (
    <div className="space-y-6">
      {/* Risk Score Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Risk Assessment</span>
            <Badge className={getRiskLevelColor(risk_level)}>
              {risk_level}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <svg className="transform -rotate-90 w-32 h-32">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-gray-200"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${(overall_risk_score / 100) * 351.86} 351.86`}
                  className={getRiskScoreColor(overall_risk_score)}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className={`text-3xl font-bold ${getRiskScoreColor(overall_risk_score)}`}>
                    {formatRiskScore(overall_risk_score)}
                  </div>
                  <div className="text-xs text-gray-500">/ 100</div>
                </div>
              </div>
            </div>
          </div>

          {risk_summary && (
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  Executive Summary
                </h4>
                <p className="text-sm text-gray-600">
                  {risk_summary.executive_summary}
                </p>
              </div>

              {risk_summary.top_3_concerns && risk_summary.top_3_concerns.length > 0 && (
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Top Concerns
                  </h4>
                  <ul className="space-y-1">
                    {risk_summary.top_3_concerns.map((concern, idx) => (
                      <li key={idx} className="text-sm text-gray-600 flex items-start">
                        <AlertTriangle className="h-4 w-4 mr-2 text-orange-500 flex-shrink-0 mt-0.5" />
                        {concern}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Key Metrics */}
      {key_metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Affected Suppliers</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    {key_metrics.total_affected || 0}
                  </p>
                </div>
                <Users className="h-8 w-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Critical Suppliers</p>
                  <p className="text-2xl font-bold text-red-600 mt-1">
                    {key_metrics.critical_affected || 0}
                  </p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Tier 1 Affected</p>
                  <p className="text-2xl font-bold text-orange-600 mt-1">
                    {key_metrics.tier_1_affected || 0}
                  </p>
                </div>
                <TrendingUp className="h-8 w-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Avg Impact Score</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">
                    {formatRiskScore(key_metrics.average_impact_score || 0)}
                  </p>
                </div>
                <TrendingUp className="h-8 w-8 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Financial Impact */}
      {financial_impact && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <DollarSign className="h-5 w-5 mr-2" />
              Financial Impact Assessment
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Daily Revenue at Risk</span>
                  <span className="text-sm font-semibold text-red-600">
                    {formatCurrency(financial_impact.daily_revenue_at_risk)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Resolution Timeline</span>
                  <span className="text-sm font-semibold">
                    {financial_impact.estimated_resolution_days} days
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Total Est. Loss</span>
                  <span className="text-sm font-semibold text-red-600">
                    {formatCurrency(financial_impact.total_estimated_loss)}
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Expedited Shipping</span>
                  <span className="text-sm font-semibold">
                    {formatCurrency(financial_impact.expedited_shipping_cost)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Alternative Sourcing</span>
                  <span className="text-sm font-semibold">
                    {formatCurrency(financial_impact.alternative_sourcing_cost)}
                  </span>
                </div>
                <div className="flex justify-between pt-3 border-t">
                  <span className="text-sm font-semibold text-gray-900">Net Impact</span>
                  <span className={`text-sm font-bold ${
                    financial_impact.net_impact > 0 ? 'text-red-600' : 'text-green-600'
                  }`}>
                    {formatCurrency(Math.abs(financial_impact.net_impact))}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Affected Suppliers List */}
      {affectedSuppliers && affectedSuppliers.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Affected Suppliers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-3 font-medium text-gray-700">Supplier</th>
                    <th className="text-left p-3 font-medium text-gray-700">Location</th>
                    <th className="text-left p-3 font-medium text-gray-700">Criticality</th>
                    <th className="text-left p-3 font-medium text-gray-700">Impact Score</th>
                    <th className="text-left p-3 font-medium text-gray-700">Reason</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {affectedSuppliers.map((supplier, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="p-3 font-medium">{supplier.supplier_name}</td>
                      <td className="p-3 text-gray-600">
                        {supplier.city && `${supplier.city}, `}{supplier.country}
                      </td>
                      <td className="p-3">
                        <Badge className={`${getRiskLevelColor(supplier.criticality.toUpperCase())} text-xs`}>
                          {supplier.criticality}
                        </Badge>
                      </td>
                      <td className="p-3">
                        <span className={`font-semibold ${getRiskScoreColor(supplier.impact_score)}`}>
                          {formatRiskScore(supplier.impact_score)}
                        </span>
                      </td>
                      <td className="p-3 text-gray-600 text-xs">
                        {supplier.impact_reason}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RiskAssessmentDisplay;