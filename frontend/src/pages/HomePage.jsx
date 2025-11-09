import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Building2 } from 'lucide-react';
import { organizationsAPI } from '../services/api';
import OrganizationCard from '../components/organization/OrganizationCard';
import OrganizationForm from '../components/organization/OrganizationForm';
import Button from '../components/ui/Button';
import Spinner from '../components/ui/Spinner';
import Alert, { AlertTitle, AlertDescription } from '../components/ui/Alert';

const HomePage = () => {
  const [showForm, setShowForm] = useState(false);
  const queryClient = useQueryClient();

  // Fetch organizations
  const { data: organizations, isLoading, error } = useQuery({
    queryKey: ['organizations'],
    queryFn: async () => {
      const response = await organizationsAPI.getAll();
      return response.data;
    },
  });

  // Create organization mutation
  const createMutation = useMutation({
    mutationFn: (data) => organizationsAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['organizations']);
      setShowForm(false);
    },
  });

  const handleCreateOrganization = async (formData) => {
    await createMutation.mutateAsync(formData);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          Failed to load organizations. Please try again.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Organizations</h1>
          <p className="text-gray-600 mt-1">
            Monitor and manage supply chain risks across your organizations
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Add Organization
        </Button>
      </div>

      {/* Stats Overview */}
      {organizations && organizations.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Organizations</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">
                  {organizations.length}
                </p>
              </div>
              <Building2 className="h-8 w-8 text-primary" />
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg border">
            <div>
              <p className="text-sm text-gray-600">Average Risk Score</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {(
                  organizations.reduce((sum, org) => sum + org.current_risk_score, 0) /
                  organizations.length
                ).toFixed(1)}
              </p>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg border">
            <div>
              <p className="text-sm text-gray-600">High Risk Organizations</p>
              <p className="text-2xl font-bold text-red-600 mt-1">
                {organizations.filter(org => org.current_risk_score >= 60).length}
              </p>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg border">
            <div>
              <p className="text-sm text-gray-600">Low Risk Organizations</p>
              <p className="text-2xl font-bold text-green-600 mt-1">
                {organizations.filter(org => org.current_risk_score < 40).length}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Organization Form */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <OrganizationForm
              onSubmit={handleCreateOrganization}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}

      {/* Organizations Grid */}
      {organizations && organizations.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {organizations.map((org) => (
            <OrganizationCard key={org.id} organization={org} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-lg border">
          <Building2 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No organizations yet
          </h3>
          <p className="text-gray-500 mb-4">
            Get started by adding your first organization
          </p>
          <Button onClick={() => setShowForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Organization
          </Button>
        </div>
      )}
    </div>
  );
};

export default HomePage;