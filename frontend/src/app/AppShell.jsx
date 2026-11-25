import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { Bell, ChevronDown, CircleHelp, LayoutDashboard, Leaf, Menu, Search, Sprout, Store, X } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../state/AuthContext.jsx';
import { DJANGO_ADMIN_URL } from '../api/client.js';

const pageNames = { '/dashboard': 'Overview', '/listings': 'Crop listings', '/market': 'Market prices', '/inbox': 'Your conversations', '/account': 'Your account' };
export function AppShell() {
  const { user } = useAuth(); const location = useLocation(); const navigate = useNavigate(); const [menuOpen, setMenuOpen] = useState(false);
  const farmer = user?.role === 'FARMER';
  const admin = user?.role === 'ADMIN';
  const nav = admin
    ? [{ to: '/dashboard', label: 'Admin overview', icon: LayoutDashboard }, { to: '/market', label: 'Market data', icon: Leaf }]
    : [{ to: '/dashboard', label: 'Overview', icon: LayoutDashboard }, { to: '/listings', label: farmer ? 'My crop listings' : 'Browse crops', icon: farmer ? Sprout : Store }, { to: '/market', label: 'Market prices', icon: Leaf }, { to: '/inbox', label: 'Enquiries & offers', icon: Bell }];
  const initials = `${user?.first_name?.[0] || user?.username?.[0] || 'K'}${user?.last_name?.[0] || ''}`.toUpperCase();
  return <div className="app-layout">
    <aside className={`sidebar ${menuOpen ? 'sidebar--open' : ''}`}><div className="sidebar__brand"><span className="brand-mark">K</span><span><strong>KrishiConnect</strong><small>Closer to a fair harvest</small></span><button className="icon-button sidebar__close" onClick={() => setMenuOpen(false)} aria-label="Close menu"><X size={19} /></button></div>
      <div className="workspace-label">{admin ? 'ADMINISTRATION' : 'WORKSPACE'}</div><nav className="side-nav" aria-label="Main navigation">{nav.map(({ to, label, icon: Icon }) => <NavLink onClick={() => setMenuOpen(false)} className={({ isActive }) => `side-nav__link ${isActive ? 'side-nav__link--active' : ''}`} to={to} key={to}><Icon size={18} strokeWidth={1.8} /><span>{label}</span>{to === '/inbox' && <i className="nav-dot" />}</NavLink>)}{admin && <a className="side-nav__link" href={DJANGO_ADMIN_URL} target="_blank" rel="noreferrer"><CircleHelp size={18} /><span>Django Admin</span></a>}</nav>
      <div className="sidebar__bottom"><div className="help-card"><span className="help-card__icon"><CircleHelp size={17} /></span><strong>Need a hand?</strong><p>We’re here to help you get started.</p><a href="mailto:support@krishiconnect.in">Get in touch <span>↗</span></a></div><div className="sidebar__footer">Growing together, every season <span>✳</span></div></div>
    </aside>{menuOpen && <button className="mobile-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
    <div className="main-area"><header className="topbar"><button className="mobile-menu icon-button" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu size={21} /></button><div className="breadcrumbs"><span>Workspace</span><b>/</b><strong>{pageNames[location.pathname] || 'Overview'}</strong></div><div className="topbar__right">{!admin && <label className="quick-search"><Search size={16} /><input aria-label="Search listings" placeholder="Search crops, markets…" onKeyDown={(event) => event.key === 'Enter' && navigate(`/listings?search=${encodeURIComponent(event.currentTarget.value)}`)} /></label>}{!admin && <button className="icon-button notification-button" aria-label="Open conversations" onClick={() => navigate('/inbox')}><Bell size={19} /><i /></button>}<button className="profile-chip" onClick={() => navigate('/account')}><span className="avatar">{initials}</span><span className="profile-chip__name">{user?.first_name || user?.username}<small>{farmer ? 'Farmer account' : user?.role === 'BUYER' ? 'Buyer account' : 'Admin account'}</small></span><ChevronDown size={15} /></button></div></header><main className="page-content"><Outlet /></main></div>
  </div>;
}
