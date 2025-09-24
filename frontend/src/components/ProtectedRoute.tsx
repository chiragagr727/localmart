import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../auth/KeycloakProvider'

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { authenticated } = useAuth()
  if (!authenticated) return <Navigate to="/" replace />
  return children
}
