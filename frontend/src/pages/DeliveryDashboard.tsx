import React from 'react'

export function DeliveryDashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Delivery Partner Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Assigned Orders</div>
          <div className="mt-2 space-y-2">
            <div className="p-3 border rounded">No orders assigned yet.</div>
          </div>
        </div>
        <div className="bg-white border rounded-lg p-4 shadow-sm">
          <div className="text-sm text-gray-500">Delivery History</div>
          <div className="mt-2 space-y-2">
            <div className="p-3 border rounded">No history available.</div>
          </div>
        </div>
      </div>
    </div>
  )
}
