import { useEffect, useState } from 'react';
import { LogOut, Save, UserRound } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../state/AuthContext.jsx';
import { profileApi } from '../api/services.js';
import { useRequest } from '../hooks/useRequest.js';
import { ErrorState, LoadingState, Notice } from '../components/Feedback.jsx';
import { FormField } from '../components/FormField.jsx';

export function AccountPage() {
  const { user, logout } = useAuth(); const navigate = useNavigate(); const farmer = user?.role === 'FARMER';
  const request = useRequest(() => farmer ? profileApi.farmer() : profileApi.buyer(), [farmer]);
  const profile = request.data; const [form, setForm] = useState({}); const [busy, setBusy] = useState(false); const [message, setMessage] = useState(''); const [error, setError] = useState('');
  useEffect(() => { if (profile) setForm(profile); }, [profile]);
  function change(event) { setForm({ ...form, [event.target.name]: event.target.value }); setMessage(''); setError(''); }
  async function save(event) { event.preventDefault(); setBusy(true); setError(''); try { await (farmer ? profileApi.updateFarmer(form) : profileApi.updateBuyer(form)); await request.reload(); setMessage('Your profile has been updated.'); } catch (err) { setError(err.message); } finally { setBusy(false); } }
  async function signOut() { await logout(); navigate('/'); }
  if (request.loading) return <LoadingState label="Loading your account…" />;
  if (request.error) return <ErrorState message={request.error} onRetry={request.reload} />;
  return <div className="account-page"><div className="page-heading"><div><span className="eyebrow">YOUR DETAILS, YOUR WAY</span><h1>Your account</h1><p>Keep your contact and location details current so good connections can find you.</p></div></div><div className="account-layout"><aside className="account-summary"><span className="account-avatar"><UserRound size={25} /></span><h2>{user?.first_name} {user?.last_name}</h2><p>@{user?.username}</p><span className="account-role">{farmer ? 'Farmer' : 'Buyer'}</span><div className="account-summary__divider" /><p className="account-summary__email">{user?.email}</p><button className="text-button text-button--danger" onClick={signOut}><LogOut size={15} /> Sign out</button></aside><section className="panel account-form-panel"><div className="panel__heading"><div><span className="eyebrow">PROFILE INFORMATION</span><h2>{farmer ? 'Farm contact details' : 'Business contact details'}</h2></div></div><Notice>{message}</Notice><Notice tone="danger">{error}</Notice><form onSubmit={save} className="form-stack"><div className="form-grid">{!farmer && <FormField name="business_name" label="Business name" value={form.business_name || ''} onChange={change} required />}<FormField name="phone" label="Phone number" value={form.phone || ''} onChange={change} required /><FormField name="state" label="State" value={form.state || ''} onChange={change} required /><FormField name="district" label="District" value={form.district || ''} onChange={change} required />{farmer && <><FormField name="village" label="Village" value={form.village || ''} onChange={change} /><FormField name="pincode" label="PIN code" value={form.pincode || ''} onChange={change} /><FormField name="land_area" label="Land area" type="number" min="0" step="0.01" value={form.land_area || ''} onChange={change} /><FormField name="land_area_unit" label="Area unit" value={form.land_area_unit || 'ACRE'} onChange={change} /></>}<FormField as="textarea" name="address" label="Address" value={form.address || ''} onChange={change} rows={3} required /></div>{!farmer && <p className="field__hint">Buyer type: {form.buyer_type?.toLowerCase()}</p>}<div className="form-actions"><button className="button button--primary" disabled={busy}>{busy ? 'Saving…' : 'Save changes'} <Save size={15} /></button></div></form></section></div></div>;
}
