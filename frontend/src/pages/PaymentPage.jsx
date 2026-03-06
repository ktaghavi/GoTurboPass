import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { paymentAPI } from '../utils/api'

export default function PaymentPage() {
  const location = useLocation()
  const navigate  = useNavigate()

  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  // Detect ?payment=cancelled when Stripe sends the user back after abandoning checkout
  const params    = new URLSearchParams(location.search)
  const cancelled = params.get('payment') === 'cancelled'

  // Optional display info passed from EnrollmentPage
  const { citationId } = location.state || {}

  /**
   * Kick off the Stripe Checkout flow:
   *   1. POST /api/payment/create-session  (JWT injected automatically by api.js)
   *   2. Redirect browser to Stripe-hosted checkout page
   *   3. On success → Stripe redirects to /dashboard?payment=success
   *   4. On cancel  → Stripe redirects to /payment?payment=cancelled  (back here)
   */
  const handlePayNow = async () => {
    setLoading(true)
    setError(null)
    try {
      const { url } = await paymentAPI.createSession()
      window.location.href = url   // full browser navigation — leaves React app
    } catch (err) {
      setError(err.message || 'Could not start checkout. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-md rounded-lg p-6 md:p-8 w-full max-w-lg">

        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-semibold text-slate-800">Secure Checkout</h1>
          <p className="text-sm text-slate-500 mt-1">
            GoTurboPass · CA DMV-Approved Traffic School
          </p>
        </div>

        {/* Cancelled banner */}
        {cancelled && (
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-yellow-800 text-sm">
            Your payment was cancelled. You can try again whenever you&apos;re ready.
          </div>
        )}

        {/* Error banner */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Order summary */}
        <div className="border border-slate-200 rounded-lg p-4 mb-6 space-y-2 text-sm text-slate-700">
          <div className="flex justify-between font-medium">
            <span>Online Traffic School Course</span>
            <span>$5.00</span>
          </div>
          <p className="text-slate-500 text-xs">CA DMV OL-613 compliant · 340-minute course</p>
          {citationId && (
            <div className="flex justify-between text-slate-400 text-xs pt-2 border-t border-slate-100">
              <span>Citation reference #{citationId}</span>
            </div>
          )}
          <div className="flex justify-between font-bold text-base pt-2 border-t border-slate-200">
            <span>Total due today</span>
            <span>$5.00</span>
          </div>
        </div>

        {/* Pay button */}
        <button
          onClick={handlePayNow}
          disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-300 text-white font-semibold py-3 rounded-lg transition text-base"
        >
          {loading ? 'Redirecting to Stripe…' : 'Pay $5.00 — Start Course'}
        </button>

        <p className="text-xs text-center text-slate-400 mt-4">
          Payments processed securely by Stripe. We never store your card details.
        </p>

        <div className="mt-4 text-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="text-xs text-slate-400 hover:text-slate-600 underline"
          >
            I already paid — go to dashboard
          </button>
        </div>
      </div>
    </div>
  )
}
