import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from '../state/AuthContext.jsx';
import { AppShell } from './AppShell.jsx';
import { LandingPage } from '../pages/LandingPage.jsx';
import { LoginPage } from '../pages/LoginPage.jsx';
import { RegisterPage } from '../pages/RegisterPage.jsx';
import { DashboardPage } from '../pages/DashboardPage.jsx';
import { ListingsPage } from '../pages/ListingsPage.jsx';
import { MarketPage } from '../pages/MarketPage.jsx';
import { InboxPage } from '../pages/InboxPage.jsx';
import { AccountPage } from '../pages/AccountPage.jsx';
import { AdminDashboardPage } from '../pages/AdminDashboardPage.jsx';
import { LoadingState } from '../components/Feedback.jsx';

function Protected({ children }) { const { user, ready } = useAuth(); if (!ready) return <LoadingState />; return user ? children : <Navigate to="/login" replace />; }
export function App() {
  const { ready, user } = useAuth();
  if (!ready) return <div className="boot-screen"><div className="brand-mark">K</div><LoadingState label="Opening your market…" /></div>;
  return <Routes>
    <Route path="/" element={user ? <Navigate to="/dashboard" replace /> : <LandingPage />} />
    <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <LoginPage />} />
    <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <RegisterPage />} />
    <Route element={<Protected><AppShell /></Protected>}>
      <Route path="/dashboard" element={user?.role === 'ADMIN' ? <AdminDashboardPage /> : <DashboardPage />} /><Route path="/listings" element={user?.role === 'ADMIN' ? <Navigate to="/dashboard" replace /> : <ListingsPage />} />
      <Route path="/market" element={<MarketPage />} /><Route path="/inbox" element={user?.role === 'ADMIN' ? <Navigate to="/dashboard" replace /> : <InboxPage />} /><Route path="/account" element={<AccountPage />} />
    </Route>
    <Route path="*" element={<Navigate to={user ? '/dashboard' : '/'} replace />} />
  </Routes>;
}
