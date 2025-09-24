import React from 'react'

export function VendorDashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Vendor Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Products</div>
          <div className="text-2xl font-semibold">0</div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Orders</div>
          <div className="text-2xl font-semibold">0</div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Revenue</div>
          <div className="text-2xl font-semibold">₹0</div>
        </div>
      </div>
    </div>
  )
}
