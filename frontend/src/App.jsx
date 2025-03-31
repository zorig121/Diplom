// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import AuthPage from './pages/AuthPage'

function isTokenValid(token) {
  try {
    const [, payload] = token.split('.')
    const decoded = JSON.parse(atob(payload))
    const now = Math.floor(Date.now() / 1000)
    return decoded.exp && decoded.exp > now
  } catch {
    return false
  }
}

function Dashboard() {
  return <h1 style={{ color: 'white', textAlign: 'center', marginTop: '20vh' }}>Welcome to Dashboard</h1>
}

function App() {
  const token = localStorage.getItem('access_token')
  const valid = token && isTokenValid(token)

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={valid ? '/dashboard' : '/auth'} />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/dashboard" element={valid ? <Dashboard /> : <Navigate to="/auth" />} />
      </Routes>
    </Router>
  )
}

export default App
