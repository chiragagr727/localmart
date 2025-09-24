import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import Keycloak from 'keycloak-js'
import { config } from '../config'

interface AuthContextValue {
  keycloak: Keycloak | null
  authenticated: boolean
  token: string | undefined
  login: () => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [keycloak, setKeycloak] = useState<Keycloak | null>(null)
  const [authenticated, setAuthenticated] = useState(false)

  useEffect(() => {
    const kc = new Keycloak({
      url: config.keycloak.url,
      realm: config.keycloak.realm,
      clientId: config.keycloak.clientId,
    })

    kc.init({ onLoad: 'check-sso', silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html' })
      .then((auth) => {
        setKeycloak(kc)
        setAuthenticated(Boolean(auth))
        if (auth) {
          scheduleTokenUpdate(kc)
        }
      })
      .catch(() => {
        setKeycloak(kc)
        setAuthenticated(false)
      })
  }, [])

  function scheduleTokenUpdate(kc: Keycloak) {
    const update = async () => {
      try {
        const refreshed = await kc.updateToken(30)
        if (refreshed) {
          setAuthenticated(true)
        }
      } catch (e) {
        setAuthenticated(false)
      }
    }
    const interval = setInterval(update, 20000)
    return () => clearInterval(interval)
  }

  const value = useMemo<AuthContextValue>(() => ({
    keycloak,
    authenticated,
    token: keycloak?.token,
    login: () => keycloak?.login(),
    logout: () => keycloak?.logout({ redirectUri: window.location.origin }),
  }), [keycloak, authenticated])

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
