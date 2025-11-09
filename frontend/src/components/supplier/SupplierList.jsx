import React from 'react';
import { Package } from 'lucide-react';
import SupplierCard from './SupplierCard';

const SupplierList = ({ suppliers }) => {
  if (!suppliers || suppliers.length === 0) {
    return (
      <div className="text-center py-12">
        <Package className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          No suppliers yet
        </h3>
        <p className="text-gray-500">
          Add suppliers to start monitoring your supply chain.
        </p>
      </div>
    );
  }

  // Group suppliers by tier
  const suppliersByTier = suppliers.reduce((acc, supplier) => {
    const tier = supplier.tier;
    if (!acc[tier]) acc[tier] = [];
    acc[tier].push(supplier);
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      {[1, 2, 3].map(tier => {
        const tierSuppliers = suppliersByTier[tier] || [];
        if (tierSuppliers.length === 0) return null;

        return (
          <div key={tier}>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Tier {tier} Suppliers
              <span className="ml-2 text-sm font-normal text-gray-500">
                ({tierSuppliers.length})
              </span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tierSuppliers.map(supplier => (
                <SupplierCard key={supplier.id} supplier={supplier} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SupplierList;