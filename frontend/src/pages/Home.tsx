import React from 'react'

export function Home() {
  return (
    <div className="space-y-6">
      <section className="rounded-xl bg-white p-6 shadow-sm border">
        <h1 className="text-2xl font-semibold">Welcome to Local Delivery</h1>
        <p className="text-gray-600 mt-2">Hyperlocal delivery of groceries and daily needs.</p>
      </section>
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[1,2,3,4,5,6].map((i) => (
          <div key={i} className="rounded-lg bg-white p-4 shadow-sm border">
            <div className="h-24 bg-gray-100 rounded mb-3" />
            <div className="font-medium">Vendor {i}</div>
            <div className="text-sm text-gray-600">Groceries and essentials</div>
          </div>
        ))}
      </section>
    </div>
  )
}
