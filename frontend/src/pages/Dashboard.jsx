import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'
import { paymentAPI } from '../utils/api'

// Polling config for post-Stripe redirect (webhook may lag a few seconds)
const POLL_INTERVAL_MS  = 2000   // check every 2 s
const POLL_MAX_ATTEMPTS = 6      // give up after ~12 s

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate         = useNavigate()
  const location         = useLocation()

  const [paymentStatus, setPaymentStatus] = useState(null)   // null = loading
  const [pollTimedOut,  setPollTimedOut]  = useState(false)

  // Detect ?payment=success when Stripe redirects the user back
  const params       = new URLSearchParams(location.search)
  const returnedPaid = params.get('payment') === 'success'

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  /**
   * Fetch /api/payment/status once; update state and return paid boolean.
   */
  const checkPayment = useCallback(async () => {
    try {
      const data = await paymentAPI.getStatus()
      setPaymentStatus(data)
      return data.paid
    } catch {
      setPaymentStatus({ paid: false, status: null })
      return false
    }
  }, [])

  /**
   * On mount:
   * - Returning from Stripe (?payment=success) → poll until paid or timeout
   * - Normal load → single fetch
   */
  useEffect(() => {
    if (!returnedPaid) {
      checkPayment()
      return
    }

    let attempts = 0
    const poll = async () => {
      attempts++
      const paid = await checkPayment()
      if (paid || attempts >= POLL_MAX_ATTEMPTS) {
        if (!paid) setPollTimedOut(true)
        clearInterval(interval)
      }
    }

    poll()
    const interval = setInterval(poll, POLL_INTERVAL_MS)
    return () => clearInterval(interval)
  }, [returnedPaid, checkPayment])

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading…</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Nav */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold">GoTurboPass</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                {user.full_name} ({user.role})
              </span>
              <button onClick={handleLogout} className="btn-secondary">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold mb-4">Welcome, {user.full_name}!</h2>
          <p className="text-gray-600">
            You are logged in as <strong>{user.role}</strong>.
          </p>
          {user.email_verified ? (
            <p className="text-green-600 mt-2">Email verified ✓</p>
          ) : (
            <p className="text-yellow-600 mt-2">Email not verified</p>
          )}
        </div>

        {/* Loading payment state */}
        {paymentStatus === null && (
          <div className="card text-center text-gray-400 py-8">
            {returnedPaid ? 'Confirming your payment…' : 'Loading course access…'}
          </div>
        )}

        {/* Webhook timed out after returning from Stripe */}
        {pollTimedOut && !paymentStatus?.paid && (
          <div className="card mb-6 border border-yellow-300 bg-yellow-50">
            <p className="text-yellow-800 font-semibold">Payment confirmation is taking a moment.</p>
            <p className="text-yellow-700 text-sm mt-1">
              Your card was charged. Refresh the page to unlock your course.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="mt-3 px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded text-sm"
            >
              Refresh
            </button>
          </div>
        )}

        {/* Payment confirmed banner */}
        {paymentStatus?.paid && returnedPaid && (
          <div className="card mb-6 border border-green-300 bg-green-50">
            <p className="text-green-800 font-semibold">
              ✓ Payment confirmed! Your course is now unlocked.
            </p>
          </div>
        )}

        {/* ── PAYWALL: not paid ── */}
        {paymentStatus !== null && !paymentStatus.paid && !pollTimedOut && (
          <div className="card mb-6">
            <h3 className="text-xl font-bold mb-2">Unlock Your Course</h3>
            <p className="text-gray-600 mb-4">
              Complete your $5.00 payment to access all 12 modules of your
              CA DMV-approved online traffic school.
            </p>
            <button
              onClick={() => navigate('/payment')}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition"
            >
              Pay Now — $5.00
            </button>
          </div>
        )}

        {/* ── COURSE MODULES: paid ── */}
        {paymentStatus?.paid && (
          <div className="card">
            <h3 className="text-xl font-bold mb-4">Course Modules</h3>
            <p className="text-gray-500 text-sm mb-4">
              Module delivery is coming in the next sprint. Your full 340-minute
              course will appear here.
            </p>
            <div className="space-y-3">
              {[
                'Introduction to Traffic Safety',
                'Speed Limits and Right-of-Way',
                'DUI and Impaired Driving',
                'Distracted Driving',
                'Sharing the Road',
              ].map((title, i) => (
                <div
                  key={i}
                  className="border border-gray-200 rounded-lg p-4 flex items-center justify-between"
                >
                  <div>
                    <h4 className="font-medium">Module {i + 1}: {title}</h4>
                    <p className="text-sm text-gray-500">~28 min · 4 quiz questions</p>
                  </div>
                  <span className={`font-medium text-sm ${i === 0 ? 'text-blue-600' : 'text-gray-400'}`}>
                    {i === 0 ? 'Start' : 'Locked'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
