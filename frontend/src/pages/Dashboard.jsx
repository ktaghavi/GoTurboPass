import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
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

        <div className="card">
          <h3 className="text-xl font-bold mb-4">Course Modules</h3>
          <p className="text-gray-600 mb-4">
            Phase 1 placeholder - module navigation will be implemented in Phase 2.
          </p>
          <div className="space-y-3">
            <div className="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
              <div>
                <h4 className="font-medium">Module 1: Introduction to Traffic Safety</h4>
                <p className="text-sm text-gray-500">10 min timer + 4 quiz questions</p>
              </div>
              <span className="text-blue-600 font-medium">Locked</span>
            </div>
            <div className="border border-gray-200 rounded-lg p-4 flex items-center justify-between opacity-50">
              <div>
                <h4 className="font-medium">Module 2: Speed Limits and Right-of-Way</h4>
                <p className="text-sm text-gray-500">10 min timer + 4 quiz questions</p>
              </div>
              <span className="text-gray-400 font-medium">Locked</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
