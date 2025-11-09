import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, CheckCircle2, Circle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import Badge from '../ui/Badge';

const PlaybookDisplay = ({ playbook }) => {
  const [expandedPhases, setExpandedPhases] = useState([0]); // First phase expanded by default

  if (!playbook) return null;

  const togglePhase = (index) => {
    setExpandedPhases(prev =>
      prev.includes(index)
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const getPriorityColor = (priority) => {
    const colors = {
      critical: 'text-red-600 bg-red-100',
      high: 'text-orange-600 bg-orange-100',
      medium: 'text-yellow-600 bg-yellow-100',
      low: 'text-blue-600 bg-blue-100'
    };
    return colors[priority] || colors.medium;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <BookOpen className="h-5 w-5 mr-2 text-purple-500" />
          Incident Response Playbook
        </CardTitle>
        <p className="text-sm text-gray-600 mt-2">
          {playbook.incident_summary}
        </p>
        <div className="flex items-center space-x-2 mt-2">
          <Badge className={`${playbook.risk_level === 'CRITICAL' ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800'}`}>
            {playbook.risk_level} Risk
          </Badge>
          <span className="text-xs text-gray-500">
            Playbook ID: {playbook.playbook_id}
          </span>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Phases */}
        <div className="space-y-4">
          {playbook.phases && playbook.phases.map((phase, phaseIdx) => (
            <div key={phaseIdx} className="border rounded-lg overflow-hidden">
              <button
                onClick={() => togglePhase(phaseIdx)}
                className="w-full p-4 bg-gray-50 hover:bg-gray-100 transition-colors flex items-center justify-between"
              >
                <div className="text-left">
                  <h4 className="font-semibold text-gray-900">{phase.phase}</h4>
                  <p className="text-sm text-gray-600 mt-1">{phase.objective}</p>
                  <p className="text-xs text-gray-500 mt-1">Timeline: {phase.timeline}</p>
                </div>
                {expandedPhases.includes(phaseIdx) ? (
                  <ChevronUp className="h-5 w-5 text-gray-400" />
                ) : (
                  <ChevronDown className="h-5 w-5 text-gray-400" />
                )}
              </button>

              {expandedPhases.includes(phaseIdx) && (
                <div className="p-4 space-y-3">
                  {phase.actions.map((action, actionIdx) => (
                    <div
                      key={actionIdx}
                      className="flex items-start space-x-3 p-3 bg-white border rounded-lg"
                    >
                      <Circle className="h-5 w-5 text-gray-400 flex-shrink-0 mt-0.5" />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {action.action}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <span className="text-xs text-gray-600">
                            Owner: {action.owner}
                          </span>
                          <span className="text-gray-300">•</span>
                          <Badge className={`text-xs ${getPriorityColor(action.priority)}`}>
                            {action.priority}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Success Metrics */}
        {playbook.success_metrics && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Success Metrics</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {playbook.success_metrics.map((metric, idx) => (
                <div key={idx} className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <p className="text-sm font-medium text-gray-900">{metric.metric}</p>
                  <p className="text-sm text-gray-600 mt-1">Target: {metric.target}</p>
                  <Badge className="mt-2 text-xs">
                    {metric.importance}
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Escalation Criteria */}
        {playbook.escalation_criteria && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Escalation Criteria</h4>
            <div className="space-y-2">
              {playbook.escalation_criteria.map((criteria, idx) => (
                <div key={idx} className="flex items-start space-x-2 p-2 bg-red-50 rounded">
                  <CheckCircle2 className="h-4 w-4 text-red-500 flex-shrink-0 mt-0.5" />
                  <span className="text-sm text-gray-700">{criteria}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Communication Plan */}
        {playbook.communication_plan && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Communication Plan</h4>
            
            {playbook.communication_plan.internal_stakeholders && (
              <div className="mb-4">
                <h5 className="text-sm font-medium text-gray-700 mb-2">Internal Stakeholders</h5>
                <div className="space-y-2">
                  {playbook.communication_plan.internal_stakeholders.map((stakeholder, idx) => (
                    <div key={idx} className="p-3 bg-gray-50 rounded-lg text-sm">
                      <p className="font-medium text-gray-900">{stakeholder.stakeholder}</p>
                      <p className="text-gray-600 mt-1">
                        Frequency: {stakeholder.frequency} • Method: {stakeholder.method}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {playbook.communication_plan.external_stakeholders && (
              <div>
                <h5 className="text-sm font-medium text-gray-700 mb-2">External Stakeholders</h5>
                <div className="space-y-2">
                  {playbook.communication_plan.external_stakeholders.map((stakeholder, idx) => (
                    <div key={idx} className="p-3 bg-gray-50 rounded-lg text-sm">
                      <p className="font-medium text-gray-900">{stakeholder.stakeholder}</p>
                      <p className="text-gray-600 mt-1">
                        Frequency: {stakeholder.frequency} • Method: {stakeholder.method}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default PlaybookDisplay;