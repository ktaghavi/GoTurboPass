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

    // In case of 204 or empty body, avoid JSON parse errors
    if (response.status === 204) {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      return null
    }

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
  // Phase 1: our backend register only expects { email, password }
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
 * GEO API — counties & courts for dropdowns
 */
export const geoAPI = {
  getCounties: () =>
    apiRequest('/api/geo/counties', {
      method: 'GET',
    }),

  getCourtsByCounty: (countyId) =>
    apiRequest(`/api/geo/courts?county_id=${countyId}`, {
      method: 'GET',
    }),
}

/**
 * Student / Enrollment API
 */
export const studentAPI = {
  // Phase 2: add module, quiz, exam APIs here later

  // Phase 1: enrollment (StudentProfile + Citation)
  enroll: (payload) =>
    apiRequest('/api/enroll', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
}

export default apiRequest
