export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  websocketUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
  keycloak: {
    url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8080',
    realm: import.meta.env.VITE_KEYCLOAK_REALM || 'local-delivery',
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'local-delivery-app',
  },
  razorpayKey: import.meta.env.VITE_RAZORPAY_KEY_ID || '',
}
