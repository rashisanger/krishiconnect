import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { accountApi } from '../api/services.js';
import { tokenStore } from '../api/client.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const loadProfile = useCallback(async () => {
    if (!tokenStore.getAccess() && !tokenStore.getRefresh()) { setUser(null); setReady(true); return; }
    try { const result = await accountApi.profile(); setUser(result.user); }
    catch { tokenStore.clear(); setUser(null); }
    finally { setReady(true); }
  }, []);
  useEffect(() => {
    loadProfile();
    const expire = () => { tokenStore.clear(); setUser(null); };
    window.addEventListener('kc:session-expired', expire);
    return () => window.removeEventListener('kc:session-expired', expire);
  }, [loadProfile]);
  const login = async (credentials) => {
    tokenStore.set(await accountApi.login(credentials));
    const result = await accountApi.profile(); setUser(result.user); return result.user;
  };
  const logout = async () => {
    const refresh = tokenStore.getRefresh();
    try { if (refresh && tokenStore.getAccess()) await accountApi.logout(refresh); }
    finally { tokenStore.clear(); setUser(null); }
  };
  const value = useMemo(() => ({ user, ready, login, logout, refreshUser: loadProfile }), [user, ready, loadProfile]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used within AuthProvider');
  return value;
}
