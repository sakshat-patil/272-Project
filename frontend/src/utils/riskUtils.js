export const getRiskLevelColor = (level) => {
  const colors = {
    MINIMAL: 'bg-green-100 text-green-800 border-green-300',
    LOW: 'bg-blue-100 text-blue-800 border-blue-300',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    HIGH: 'bg-orange-100 text-orange-800 border-orange-300',
    CRITICAL: 'bg-red-100 text-red-800 border-red-300'
  };
  return colors[level] || colors.MEDIUM;
};

export const getRiskScoreColor = (score) => {
  if (score >= 80) return 'text-red-600';
  if (score >= 60) return 'text-orange-600';
  if (score >= 40) return 'text-yellow-600';
  if (score >= 20) return 'text-blue-600';
  return 'text-green-600';
};

export const getCriticalityColor = (criticality) => {
  const colors = {
    Critical: 'bg-red-500',
    High: 'bg-orange-500',
    Medium: 'bg-yellow-500',
    Low: 'bg-green-500'
  };
  return colors[criticality] || colors.Medium;
};

export const formatRiskScore = (score) => {
  return Math.round(score * 10) / 10;
};

export const getRiskGaugeColor = (score) => {
  if (score >= 80) return '#dc2626'; // red-600
  if (score >= 60) return '#ea580c'; // orange-600
  if (score >= 40) return '#ca8a04'; // yellow-600
  if (score >= 20) return '#2563eb'; // blue-600
  return '#16a34a'; // green-600
};