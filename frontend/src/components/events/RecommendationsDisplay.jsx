import React from 'react';
import { Lightbulb, CheckCircle2, Clock, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Badge from '../ui/Badge';

const RecommendationsDisplay = ({ recommendations, alternativeSuppliers }) => {
  if (!recommendations) return null;

  const { strategic_recommendations, immediate_actions, long_term_strategies } = recommendations;

  const getPriorityColor = (priority) => {
    const colors = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800'
    };
    return colors[priority] || colors.medium;
  };

  return (
    <div className="space-y-6">
      {/* Strategic Recommendations */}
      {strategic_recommendations && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
              Strategic Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Immediate Actions */}
            {strategic_recommendations.immediate_actions && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <Clock className="h-4 w-4 mr-2 text-red-500" />
                  Immediate Actions (0-24 hours)
                </h4>
                <div className="space-y-2">
                  {strategic_recommendations.immediate_actions.map((action, idx) => (
                    <div key={idx} className="flex items-start space-x-3 p-3 bg-red-50 rounded-lg">
                      <CheckCircle2 className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {action.action}
                        </p>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge className={getPriorityColor(action.priority)}>
                            {action.priority}
                          </Badge>
                          <span className="text-xs text-gray-500">
                            {action.timeline}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Short-term Strategies */}
            {strategic_recommendations.short_term_strategies && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <TrendingUp className="h-4 w-4 mr-2 text-orange-500" />
                  Short-term Strategies (1-7 days)
                </h4>
                <div className="space-y-2">
                  {strategic_recommendations.short_term_strategies.map((strategy, idx) => (
                    <div key={idx} className="p-3 bg-orange-50 rounded-lg">
                      <p className="text-sm font-medium text-gray-900">
                        {strategy.strategy}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Expected Impact: {strategy.expected_impact}
                      </p>
                      <span className="text-xs text-gray-500">
                        Timeline: {strategy.timeline}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Long-term Improvements */}
            {strategic_recommendations.long_term_improvements && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <Lightbulb className="h-4 w-4 mr-2 text-blue-500" />
                  Long-term Improvements (1+ months)
                </h4>
                <div className="space-y-2">
                  {strategic_recommendations.long_term_improvements.map((improvement, idx) => (
                    <div key={idx} className="p-3 bg-blue-50 rounded-lg">
                      <p className="text-sm font-medium text-gray-900">
                        {improvement.improvement}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Rationale: {improvement.rationale}
                      </p>
                      <span className="text-xs text-gray-500">
                        Timeline: {improvement.timeline}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Alternative Suppliers */}
      {alternativeSuppliers && alternativeSuppliers.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Alternative Supplier Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {alternativeSuppliers.map((item, idx) => (
                <div key={idx} className="border-b last:border-b-0 pb-6 last:pb-0">
                  <div className="mb-3">
                    <h4 className="font-semibold text-gray-900">
                      Alternatives for: {item.affected_supplier_name}
                    </h4>
                    <p className="text-sm text-gray-600">
                      Category: {item.category}
                    </p>
                  </div>

                  <div className="space-y-3">
                    {item.alternatives.map((alt, altIdx) => (
                      <div
                        key={altIdx}
                        className="p-4 bg-green-50 rounded-lg border border-green-200"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <p className="font-medium text-gray-900">
                              {alt.supplier_name}
                            </p>
                            <p className="text-sm text-gray-600">
                              {alt.details.city && `${alt.details.city}, `}
                              {alt.details.country}
                            </p>
                          </div>
                          <div className="text-right">
                            <div className="text-2xl font-bold text-green-600">
                              {alt.total_score}
                            </div>
                            <div className="text-xs text-gray-500">Score</div>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
                          <div>
                            <span className="text-gray-600">Lead Time:</span>
                            <span className="font-medium ml-1">
                              {alt.details.lead_time_days} days
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600">Reliability:</span>
                            <span className="font-medium ml-1">
                              {alt.details.reliability_score}%
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600">Capacity:</span>
                            <span className="font-medium ml-1">
                              {100 - alt.details.capacity_utilization}% available
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-600">Tier:</span>
                            <span className="font-medium ml-1">
                              Tier {alt.details.tier}
                            </span>
                          </div>
                        </div>

                        <details className="mt-3">
                          <summary className="text-xs text-blue-600 cursor-pointer hover:text-blue-800">
                            View score breakdown
                          </summary>
                          <div className="mt-2 space-y-1">
                            {Object.entries(alt.score_breakdown).map(([key, value]) => (
                              <div key={key} className="flex justify-between text-xs">
                                <span className="text-gray-600 capitalize">
                                  {key.replace(/_/g, ' ')}:
                                </span>
                                <span className="font-medium">{value}</span>
                              </div>
                            ))}
                          </div>
                        </details>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default RecommendationsDisplay;