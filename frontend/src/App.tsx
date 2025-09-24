import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import { Home } from './pages/Home'
import { VendorDashboard } from './pages/VendorDashboard'
import { AdminDashboard } from './pages/AdminDashboard'
import { DeliveryDashboard } from './pages/DeliveryDashboard'
import { useAuth } from './auth/KeycloakProvider'
import { ProtectedRoute } from './components/ProtectedRoute'

export default function App() {
  const { authenticated, login, logout } = useAuth()
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 bg-white border-b">
        <div className="container mx-auto px-4 py-3 flex items-center gap-4">
          <Link to="/" className="text-xl font-semibold text-primary">Local Delivery</Link>
          <nav className="flex gap-4 text-sm">
            <Link to="/vendor" className="hover:underline">Vendor</Link>
            <Link to="/delivery" className="hover:underline">Delivery</Link>
            <Link to="/admin" className="hover:underline">Admin</Link>
          </nav>
          <div className="ml-auto">
            {authenticated ? (
              <button onClick={logout} className="px-3 py-1.5 rounded bg-primary text-white">Logout</button>
            ) : (
              <button onClick={login} className="px-3 py-1.5 rounded bg-primary text-white">Login</button>
            )}
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/vendor" element={<ProtectedRoute><VendorDashboard /></ProtectedRoute>} />
          <Route path="/delivery" element={<ProtectedRoute><DeliveryDashboard /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><AdminDashboard /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  )
}
