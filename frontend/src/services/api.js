import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Organizations
export const organizationsAPI = {
  getAll: () => api.get('/api/organizations'),
  getById: (id) => api.get(`/api/organizations/${id}`),
  create: (data) => api.post('/api/organizations', data),
  update: (id, data) => api.put(`/api/organizations/${id}`, data),
  delete: (id) => api.delete(`/api/organizations/${id}`),
};

// Suppliers
export const suppliersAPI = {
  getByOrganization: (orgId) => api.get(`/api/suppliers/organization/${orgId}`),
  getById: (id) => api.get(`/api/suppliers/${id}`),
  create: (data) => api.post('/api/suppliers', data),
  update: (id, data) => api.put(`/api/suppliers/${id}`, data),
  delete: (id) => api.delete(`/api/suppliers/${id}`),
  createDependency: (data) => api.post('/api/suppliers/dependencies', data),
  getDependencies: (supplierId) => api.get(`/api/suppliers/${supplierId}/dependencies`),
};

// Events
export const eventsAPI = {
  create: (data) => api.post('/api/events', data),
  getById: (id) => api.get(`/api/events/${id}`),
  getByOrganization: (orgId, params = {}) => 
    api.get(`/api/events/organization/${orgId}`, { params }),
  compare: (data) => api.post('/api/events/compare', data),
  getComparison: (comparisonId) => api.get(`/api/events/compare/${comparisonId}`),
};

// Predictions
export const predictionsAPI = {
  create: (data) => api.post('/api/predictions', data),
  getLatest: (orgId, periodDays = 90) => 
    api.get(`/api/predictions/organization/${orgId}/latest`, { 
      params: { period_days: periodDays } 
    }),
};

// Risk History
export const riskHistoryAPI = {
  getByOrganization: (orgId, days = 30) => 
    api.get(`/api/risk-history/organization/${orgId}`, { params: { days } }),
  create: (data) => api.post('/api/risk-history', data),
};

export default api;