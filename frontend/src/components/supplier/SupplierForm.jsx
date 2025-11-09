import React, { useState } from 'react';
import { X } from 'lucide-react';
import Button from '../ui/Button';
import Input from '../ui/Input';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';

const SupplierForm = ({ organizationId, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    organization_id: organizationId,
    name: '',
    country: '',
    city: '',
    category: 'Raw Materials',
    criticality: 'Medium',
    tier: 1,
    lead_time_days: 30,
    reliability_score: 85,
    capacity_utilization: 70,
    contact_info: '',
    latitude: null,
    longitude: null,
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const categories = [
    'Raw Materials',
    'Components',
    'Finished Goods',
    'Logistics',
    'Services'
  ];

  const criticalityLevels = ['Low', 'Medium', 'High', 'Critical'];
  const tiers = [1, 2, 3];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      // Convert string values to numbers where needed
      const submitData = {
        ...formData,
        tier: parseInt(formData.tier),
        lead_time_days: parseInt(formData.lead_time_days),
        reliability_score: parseFloat(formData.reliability_score),
        capacity_utilization: parseFloat(formData.capacity_utilization),
        latitude: formData.latitude ? parseFloat(formData.latitude) : null,
        longitude: formData.longitude ? parseFloat(formData.longitude) : null,
      };
      await onSubmit(submitData);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Add New Supplier</CardTitle>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      </CardHeader>
      
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Supplier Name *
              </label>
              <Input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g., TechComponents Ltd"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Country *
              </label>
              <Input
                type="text"
                name="country"
                value={formData.country}
                onChange={handleChange}
                placeholder="e.g., China"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                City
              </label>
              <Input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="e.g., Shanghai"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category *
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                required
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Criticality *
              </label>
              <select
                name="criticality"
                value={formData.criticality}
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                required
              >
                {criticalityLevels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tier *
              </label>
              <select
                name="tier"
                value={formData.tier}
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                required
              >
                {tiers.map(tier => (
                  <option key={tier} value={tier}>Tier {tier}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Lead Time (days) *
              </label>
              <Input
                type="number"
                name="lead_time_days"
                value={formData.lead_time_days}
                onChange={handleChange}
                min="1"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Reliability Score (0-100) *
              </label>
              <Input
                type="number"
                name="reliability_score"
                value={formData.reliability_score}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.1"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Capacity Utilization (%) *
              </label>
              <Input
                type="number"
                name="capacity_utilization"
                value={formData.capacity_utilization}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.1"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Latitude
              </label>
              <Input
                type="number"
                name="latitude"
                value={formData.latitude || ''}
                onChange={handleChange}
                placeholder="e.g., 31.2304"
                step="any"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Longitude
              </label>
              <Input
                type="number"
                name="longitude"
                value={formData.longitude || ''}
                onChange={handleChange}
                placeholder="e.g., 121.4737"
                step="any"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contact Info
              </label>
              <Input
                type="text"
                name="contact_info"
                value={formData.contact_info}
                onChange={handleChange}
                placeholder="e.g., contact@supplier.com"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Adding...' : 'Add Supplier'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default SupplierForm;