import { createContext, useState, useEffect, useContext, useCallback } from 'react'
import { setAccessToken, clearAccessToken, authAPI } from '../utils/api'

const AuthContext = createContext()

const IDLE_TIMEOUT = 20 * 60 * 1000 // 20 minutes

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [idleTimer, setIdleTimer] = useState(null)

  /**
   * Reset idle timer on user activity
   */
  const resetIdleTimer = useCallback(() => {
    if (idleTimer) {
      clearTimeout(idleTimer)
    }

    const timer = setTimeout(() => {
      logout()
    }, IDLE_TIMEOUT)

    setIdleTimer(timer)
  }, [idleTimer])

  /**
   * Login
   */
  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password)
      setAccessToken(response.accessToken)
      setUser(response.user)
      resetIdleTimer()
      return response.user
    } catch (error) {
      throw error
    }
  }

  /**
   * Logout
   */
  const logout = () => {
    clearAccessToken()
    setUser(null)
    if (idleTimer) {
      clearTimeout(idleTimer)
      setIdleTimer(null)
    }
  }

  /**
   * Load user from JWT (if stored elsewhere in future)
   */
  useEffect(() => {
    // Phase 1: No persistent storage, so just set loading to false
    setLoading(false)
  }, [])

  /**
   * Setup idle logout listeners
   */
  useEffect(() => {
    if (user) {
      // Reset timer on user activity
      const events = ['mousedown', 'keydown', 'scroll', 'touchstart']
      events.forEach((event) => {
        window.addEventListener(event, resetIdleTimer)
      })

      return () => {
        events.forEach((event) => {
          window.removeEventListener(event, resetIdleTimer)
        })
      }
    }
  }, [user, resetIdleTimer])

  const value = {
    user,
    loading,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
