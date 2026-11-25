import { useEffect, useMemo, useState } from 'react';
import { CalendarDays, MapPin, Search, Sprout } from 'lucide-react';
import { marketApi } from '../api/services.js';
import { unwrapPage } from '../api/client.js';
import { useRequest } from '../hooks/useRequest.js';
import { EmptyState, ErrorState, LoadingState } from '../components/Feedback.jsx';
import { FormField } from '../components/FormField.jsx';

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value || 0));
const date = (value) => value ? new Date(value).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '—';

export function MarketPage() {
  const [filters, setFilters] = useState({ crop: '', state: '', district: '', mandi: '', sort: 'date_desc' });
  const [applied, setApplied] = useState(filters);
  const request = useRequest(() => marketApi.prices(applied), [applied]);
  const rows = useMemo(() => unwrapPage(request.data), [request.data]);
  const options = useMemo(() => [...new Set(rows.map((row) => row.crop_name).filter(Boolean))], [rows]);
  useEffect(() => { if (!filters.crop && options[0]) setFilters((current) => ({ ...current, crop: options[0] })); }, [filters.crop, options]);
  function submit(event) { event.preventDefault(); setApplied(filters); }
  return <div className="market-page"><div className="page-heading"><div><span className="eyebrow">A LITTLE MARKET KNOW-HOW</span><h1>Prices from the mandi</h1><p>Recent market prices can help you start your next conversation with confidence.</p></div><div className="market-date"><CalendarDays size={16} /> Latest available records</div></div>
    <form className="market-filters" onSubmit={submit}><FormField label="Crop" name="crop" value={filters.crop} onChange={(e) => setFilters({ ...filters, crop: e.target.value })} placeholder="e.g. Onion" /><FormField label="State" name="state" value={filters.state} onChange={(e) => setFilters({ ...filters, state: e.target.value })} placeholder="Any state" /><FormField label="District" name="district" value={filters.district} onChange={(e) => setFilters({ ...filters, district: e.target.value })} placeholder="Any district" /><FormField label="Mandi" name="mandi" value={filters.mandi} onChange={(e) => setFilters({ ...filters, mandi: e.target.value })} placeholder="Any mandi" /><FormField as="select" label="Sort by" name="sort" value={filters.sort} onChange={(e) => setFilters({ ...filters, sort: e.target.value })}><option value="date_desc">Most recent</option><option value="modal_asc">Lowest modal price</option><option value="modal_desc">Highest modal price</option></FormField><button className="button button--primary"><Search size={16} /> Find prices</button></form>
    <div className="market-disclaimer"><span>i</span><p>Market prices are reported mandi prices. They’re a useful guide, not a promise of what an individual farmer will receive.</p></div>
    {request.loading ? <LoadingState label="Looking up mandi records…" /> : request.error ? <ErrorState message={request.error} onRetry={request.reload} /> : rows.length ? <div className="market-table-wrap"><table className="market-table"><thead><tr><th>Crop & variety</th><th>Market</th><th>Min price</th><th>Modal price</th><th>Max price</th><th>Reported</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id}><td><span className="table-crop"><span className="crop-avatar crop-avatar--small"><Sprout size={15} /></span><span><b>{row.crop_name}</b><small>{row.variety || 'Standard variety'}</small></span></span></td><td><span className="table-market"><b>{row.mandi}</b><small><MapPin size={11} /> {row.district}, {row.state}</small></span></td><td>{money(row.minimum_price)}</td><td><strong className="modal-price">{money(row.modal_price)}</strong></td><td>{money(row.maximum_price)}</td><td>{date(row.price_date)}</td></tr>)}</tbody></table></div> : <EmptyState title="No prices found for those filters" message="Market records are added as they’re reported. Try a broader location or another crop." action={<button className="button button--secondary button--small" onClick={() => { const cleared = { crop: '', state: '', district: '', mandi: '', sort: 'date_desc' }; setFilters(cleared); setApplied(cleared); }}>Clear filters</button>} />}
    <div className="market-footnote"><span>✳</span><p>Data is sourced from Agmarknet through the Government of India’s Open Data platform. Availability depends on the records imported into this marketplace.</p></div>
  </div>;
}
