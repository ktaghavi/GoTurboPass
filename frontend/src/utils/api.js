/**
 * API Client Wrapper
 *
 * Features:
 * - JWT token management (in-memory)
 * - Automatic token injection
 * - Error handling
 * - PII-safe logging
 */

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

let accessToken = null

/**
 * Set access token (stored in memory only)
 */
export function setAccessToken(token) {
  accessToken = token
}

/**
 * Get access token
 */
export function getAccessToken() {
  return accessToken
}

/**
 * Clear access token
 */
export function clearAccessToken() {
  accessToken = null
}

/**
 * Generic API request wrapper
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  // Inject JWT if available
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  const config = {
    ...options,
    headers,
  }

  try {
    const response = await fetch(url, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`)
    }

    return data
  } catch (error) {
    console.error(`API Error [${endpoint}]:`, error.message)
    throw error
  }
}

/**
 * Auth API
 */
export const authAPI = {
  register: (data) => apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  verify: (token) => apiRequest('/api/auth/verify', {
    method: 'POST',
    body: JSON.stringify({ token }),
  }),

  login: (email, password) => apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  }),

  me: () => apiRequest('/api/me', {
    method: 'GET',
  }),
}

/**
 * Student API (placeholder for Phase 2)
 */
export const studentAPI = {
  // TODO Phase 2: Add module, quiz, exam APIs
}

export default apiRequest
