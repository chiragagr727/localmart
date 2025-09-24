import React from 'react'

export function AdminDashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Vendors Pending KYC</div>
          <div className="text-2xl font-semibold">0</div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Orders (Today)</div>
          <div className="text-2xl font-semibold">0</div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Revenue (Today)</div>
          <div className="text-2xl font-semibold">₹0</div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Avg. Rating</div>
          <div className="text-2xl font-semibold">0.0</div>
        </div>
      </div>
    </div>
  )
}
