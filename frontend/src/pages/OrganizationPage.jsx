import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  ArrowLeft, Plus, Users, AlertTriangle, TrendingUp, 
  FileText, Calendar 
} from 'lucide-react';
import { organizationsAPI, suppliersAPI, eventsAPI } from '../services/api';
import Button from '../components/ui/Button';
import Spinner from '../components/ui/Spinner';
import Alert, { AlertTitle, AlertDescription } from '../components/ui/Alert';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import SupplierList from '../components/supplier/SupplierList';
import SupplierForm from '../components/supplier/SupplierForm';
import EventAnalyzer from '../components/events/EventAnalyzer';
import AgentActivityFeed from '../components/events/AgentActivityFeed';
import RiskAssessmentDisplay from '../components/events/RiskAssessmentDisplay';
import RecommendationsDisplay from '../components/events/RecommendationsDisplay';
import PlaybookDisplay from '../components/events/PlaybookDisplay';
import LiveMonitoringFeed from '../components/events/LiveMonitoringFeed';
import { getRiskLevelColor, formatRiskScore } from '../utils/riskUtils';
import { formatDate } from '../utils/formatters';
import AnalysisLoader from '../components/events/AnalysisLoader';

const OrganizationPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [showSupplierForm, setShowSupplierForm] = useState(false);
  const [activeTab, setActiveTab] = useState('suppliers');
  const [processingEventId, setProcessingEventId] = useState(null);
  const [pollingInterval, setPollingInterval] = useState(null);

  // Fetch organization
  const { data: organization, isLoading: orgLoading } = useQuery({
    queryKey: ['organization', id],
    queryFn: async () => {
      const response = await organizationsAPI.getById(id);
      return response.data;
    },
  });

  // Fetch suppliers
  const { data: suppliers, isLoading: suppliersLoading } = useQuery({
    queryKey: ['suppliers', id],
    queryFn: async () => {
      const response = await suppliersAPI.getByOrganization(id);
      return response.data;
    },
  });

  // Fetch events
  const { data: events } = useQuery({
    queryKey: ['events', id],
    queryFn: async () => {
      const response = await eventsAPI.getByOrganization(id);
      return response.data;
    },
  });

  // Fetch processing event details
  const { data: processingEvent } = useQuery({
    queryKey: ['event', processingEventId],
    queryFn: async () => {
      const response = await eventsAPI.getById(processingEventId);
      return response.data;
    },
    enabled: !!processingEventId,
    refetchInterval: pollingInterval,
  });

  // Create supplier mutation
  const createSupplierMutation = useMutation({
    mutationFn: (data) => suppliersAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['suppliers', id]);
      setShowSupplierForm(false);
    },
  });

  // Create event mutation
  const createEventMutation = useMutation({
    mutationFn: (data) => eventsAPI.create(data),
    onSuccess: (response) => {
      queryClient.invalidateQueries(['events', id]);
      setProcessingEventId(response.data.id);
      setActiveTab('analysis');
      setPollingInterval(2000); // Poll every 2 seconds
    },
  });

  // Stop polling when event is completed
  useEffect(() => {
    if (processingEvent && processingEvent.processing_status === 'completed') {
      setPollingInterval(null);
      queryClient.invalidateQueries(['organization', id]);
    }
  }, [processingEvent, id, queryClient]);

  const handleCreateSupplier = async (formData) => {
    await createSupplierMutation.mutateAsync(formData);
  };

  const handleAnalyzeEvent = async (eventData) => {
    await createEventMutation.mutateAsync(eventData);
  };

  const handleViewWeatherEvent = (eventId) => {
    setProcessingEventId(eventId);
    setActiveTab('analysis');
    setPollingInterval(2000); // Start polling for updates
  };

  if (orgLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!organization) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>Organization not found</AlertDescription>
      </Alert>
    );
  }

  const getRiskLevel = (score) => {
    if (score >= 80) return 'CRITICAL';
    if (score >= 60) return 'HIGH';
    if (score >= 40) return 'MEDIUM';
    if (score >= 20) return 'LOW';
    return 'MINIMAL';
  };

  const tabs = [
    { id: 'suppliers', label: 'Suppliers', icon: Users },
    { id: 'monitoring', label: 'Live Monitoring', icon: TrendingUp },
    { id: 'analysis', label: 'Event Analysis', icon: AlertTriangle },
    { id: 'history', label: 'History', icon: Calendar },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Button
          variant="ghost"
          onClick={() => navigate('/')}
          className="mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Organizations
        </Button>

        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {organization.name}
            </h1>
            <p className="text-gray-600 mt-1">
              {organization.headquarters_location} • {organization.industry}
            </p>
            {organization.description && (
              <p className="text-gray-600 mt-2 max-w-3xl">
                {organization.description}
              </p>
            )}
          </div>

          <Badge className={getRiskLevelColor(getRiskLevel(organization.current_risk_score))}>
            {getRiskLevel(organization.current_risk_score)} Risk
          </Badge>
        </div>
      </div>

      {/* Risk Score Card */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Current Risk Score</p>
              <p className="text-3xl font-bold text-gray-900 mt-1">
                {formatRiskScore(organization.current_risk_score)}
                <span className="text-lg text-gray-500">/100</span>
              </p>
            </div>
            <TrendingUp className="h-12 w-12 text-primary" />
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Suppliers</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  {suppliers?.length || 0}
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
                  {suppliers?.filter(s => s.criticality === 'Critical').length || 0}
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
                <p className="text-sm text-gray-600">Events Analyzed</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  {events?.length || 0}
                </p>
              </div>
              <FileText className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center py-4 px-1 border-b-2 font-medium text-sm
                  ${
                    activeTab === tab.id
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="h-5 w-5 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'suppliers' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Suppliers</h2>
              <Button onClick={() => setShowSupplierForm(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Supplier
              </Button>
            </div>

            {suppliersLoading ? (
              <div className="flex items-center justify-center py-12">
                <Spinner />
              </div>
            ) : (
              <SupplierList suppliers={suppliers} />
            )}
          </div>
        )}

        {activeTab === 'monitoring' && (
          <div className="space-y-6">
            <LiveMonitoringFeed 
              organizationId={id} 
              onViewEvent={handleViewWeatherEvent}
            />
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-6">
            <EventAnalyzer
              organizationId={id}
              onAnalysisComplete={handleAnalyzeEvent}
            />

            {processingEvent && (
              <>
                {processingEvent.processing_status === 'processing' && (
                  <AnalysisLoader
                    agentLogs={processingEvent.agent_logs}
                    isProcessing={true}
                  />
                )}

                {processingEvent.processing_status === 'completed' && (
                  <div className="space-y-6">
                    <Alert variant="success">
                      <AlertTitle>Analysis Complete</AlertTitle>
                      <AlertDescription>
                        Event analysis completed in{' '}
                        {processingEvent.processing_time_seconds?.toFixed(1)}s
                      </AlertDescription>
                    </Alert>

                    <AgentActivityFeed
                      agentLogs={processingEvent.agent_logs}
                      isProcessing={false}
                    />

                    <RiskAssessmentDisplay
                      riskAnalysis={processingEvent.risk_analysis}
                      affectedSuppliers={processingEvent.affected_suppliers}
                    />

                    <RecommendationsDisplay
                      recommendations={processingEvent.recommendations}
                      alternativeSuppliers={processingEvent.alternative_suppliers}
                    />

                    <PlaybookDisplay playbook={processingEvent.playbook} />
                  </div>
                )}

                {processingEvent.processing_status === 'failed' && (
                  <Alert variant="destructive">
                    <AlertTitle>Analysis Failed</AlertTitle>
                    <AlertDescription>
                      The event analysis failed. Please try again.
                    </AlertDescription>
                  </Alert>
                )}
              </>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Event History</h2>
            
            {events && events.length > 0 ? (
              <div className="space-y-4">
                {events.map((event) => (
                  <Card key={event.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge className={getRiskLevelColor(event.processing_status.toUpperCase())}>
                              {event.processing_status}
                            </Badge>
                            {event.event_type && (
                              <Badge variant="outline">{event.event_type}</Badge>
                            )}
                          </div>
                          <p className="text-gray-900 font-medium mb-2">
                            {event.event_input}
                          </p>
                          <div className="flex items-center space-x-4 text-sm text-gray-600">
                            <span>Risk Score: {formatRiskScore(event.overall_risk_score)}</span>
                            <span>•</span>
                            <span>{event.affected_supplier_count} suppliers affected</span>
                            <span>•</span>
                            <span>{formatDate(event.created_at)}</span>
                          </div>
                        </div>
                        {event.processing_status === 'completed' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setProcessingEventId(event.id);
                              setActiveTab('analysis');
                            }}
                          >
                            View Details
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 bg-white rounded-lg border">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No events analyzed yet
                </h3>
                <p className="text-gray-500 mb-4">
                  Analyze your first event to see the history here
                </p>
                <Button onClick={() => setActiveTab('analysis')}>
                  Analyze Event
                </Button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Supplier Form Modal */}
      {showSupplierForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <SupplierForm
              organizationId={parseInt(id)}
              onSubmit={handleCreateSupplier}
              onCancel={() => setShowSupplierForm(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default OrganizationPage;