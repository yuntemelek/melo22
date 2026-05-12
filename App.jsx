import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { AuthProvider, useAuth } from './context/AuthContext'
import PageTransition from './components/layout/PageTransition'
import GirisPage from './pages/GirisPage'
import KayitPage from './pages/KayitPage'
import KurulumPage from './pages/KurulumPage'
import AnaSayfaPage from './pages/AnaSayfaPage'
import PratikPage from './pages/PratikPage'
import TestPage from './pages/TestPage'
import SohbetPage from './pages/SohbetPage'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  return user ? children : <Navigate to="/giris" replace />
}

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/giris" element={<PageTransition><GirisPage /></PageTransition>} />
        <Route path="/kayit" element={<PageTransition><KayitPage /></PageTransition>} />
        <Route path="/kurulum" element={<ProtectedRoute><PageTransition><KurulumPage /></PageTransition></ProtectedRoute>} />
        <Route path="/" element={<ProtectedRoute><PageTransition><AnaSayfaPage /></PageTransition></ProtectedRoute>} />
        <Route path="/pratik" element={<ProtectedRoute><PageTransition><PratikPage /></PageTransition></ProtectedRoute>} />
        <Route path="/pratik/:topicId" element={<ProtectedRoute><PageTransition><TestPage /></PageTransition></ProtectedRoute>} />
        <Route path="/sohbet" element={<ProtectedRoute><PageTransition><SohbetPage /></PageTransition></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AnimatedRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
