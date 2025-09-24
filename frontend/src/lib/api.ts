import axios from 'axios'
import { config } from '../config'
import { useAuth } from '../auth/KeycloakProvider'

// Hook-friendly API client
export function useApi() {
  const { token } = useAuth()
  const instance = axios.create({ baseURL: config.apiBaseUrl })
  instance.interceptors.request.use((req) => {
    if (token) {
      req.headers = req.headers || {}
      req.headers.Authorization = `Bearer ${token}`
    }
    return req
  })
  return instance
}
