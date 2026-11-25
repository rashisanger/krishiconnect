import { useMemo, useState } from 'react';
import { CalendarDays, MapPin, Search, Sprout } from 'lucide-react';
import { marketApi } from '../api/services.js';
import { unwrapPage } from '../api/client.js';
import { useRequest } from '../hooks/useRequest.js';
import { EmptyState, ErrorState, LoadingState } from '../components/Feedback.jsx';
import { FormField } from '../components/FormField.jsx';
import { PaginationControls } from '../components/PaginationControls.jsx';

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value || 0));
const date = (value) => value ? new Date(value).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '—';

export function MarketPage() {
  const [filters, setFilters] = useState({ crop: '', state: '', district: '', mandi: '', sort: 'date_desc' });
  const [applied, setApplied] = useState(filters);
  const [page, setPage] = useState(1);
  const request = useRequest(() => marketApi.prices({ ...applied, page }), [applied, page]);
  const rows = useMemo(() => unwrapPage(request.data), [request.data]);
  function submit(event) { event.preventDefault(); setPage(1); setApplied(filters); }
  return <div className="market-page"><div className="page-heading"><div><span className="eyebrow">A LITTLE MARKET KNOW-HOW</span><h1>Prices from the mandi</h1><p>Recent market prices can help you start your next conversation with confidence.</p></div><div className="market-date"><CalendarDays size={16} /> Latest available records</div></div>
    <form className="market-filters" onSubmit={submit}><FormField label="Crop" name="crop" value={filters.crop} onChange={(e) => setFilters({ ...filters, crop: e.target.value })} placeholder="e.g. Onion" /><FormField label="State" name="state" value={filters.state} onChange={(e) => setFilters({ ...filters, state: e.target.value })} placeholder="Any state" /><FormField label="District" name="district" value={filters.district} onChange={(e) => setFilters({ ...filters, district: e.target.value })} placeholder="Any district" /><FormField label="Mandi" name="mandi" value={filters.mandi} onChange={(e) => setFilters({ ...filters, mandi: e.target.value })} placeholder="Any mandi" /><FormField as="select" label="Sort by" name="sort" value={filters.sort} onChange={(e) => setFilters({ ...filters, sort: e.target.value })}><option value="date_desc">Most recent</option><option value="modal_asc">Lowest modal price</option><option value="modal_desc">Highest modal price</option></FormField><button className="button button--primary"><Search size={16} /> Find prices</button></form>
    <div className="market-disclaimer"><span>i</span><p>Market prices are reported mandi prices. They’re a useful guide, not a promise of what an individual farmer will receive.</p></div>
    {!request.loading && !request.error && request.data && <div className="market-result-summary"><span>{request.data.count ?? rows.length} matching records</span><span>Latest matching report: <b>{date(request.data.latest_price_date || rows.reduce((latest, row) => !latest || row.price_date > latest ? row.price_date : latest, null))}</b></span><span>Source: {request.data.source || 'No matching source'}</span></div>}
    {request.loading ? <LoadingState label="Looking up mandi records…" /> : request.error ? <ErrorState message={request.error} onRetry={request.reload} /> : rows.length ? <><div className="market-table-wrap"><table className="market-table"><thead><tr><th>Crop & variety</th><th>Market</th><th>Min price</th><th>Modal price</th><th>Max price</th><th>Reported</th><th>Source</th></tr></thead><tbody>{rows.map((row) => <tr key={row.id}><td><span className="table-crop"><span className="crop-avatar crop-avatar--small"><Sprout size={15} /></span><span><b>{row.crop_name}</b><small>{row.variety || 'Standard variety'}</small></span></span></td><td><span className="table-market"><b>{row.mandi}</b><small><MapPin size={11} /> {row.district}, {row.state}</small></span></td><td>{money(row.minimum_price)}</td><td><strong className="modal-price">{money(row.modal_price)}</strong></td><td>{money(row.maximum_price)}</td><td>{date(row.price_date)}</td><td>{row.source}</td></tr>)}</tbody></table></div><PaginationControls page={page} count={request.data.count} pageSize={5} hasPrevious={Boolean(request.data.previous)} hasNext={Boolean(request.data.next)} onChange={setPage} /></> : <EmptyState title="No prices found for those filters" message="Market records are added as they’re reported. Try a broader location or another crop." action={<button type="button" className="button button--secondary button--small" onClick={() => { const cleared = { crop: '', state: '', district: '', mandi: '', sort: 'date_desc' }; setFilters(cleared); setApplied(cleared); setPage(1); }}>Clear filters</button>} />}
    <div className="market-footnote"><span>✳</span><p>Agmarknet records are retrieved from the Government of India Open Data platform. Demo fixtures are labeled “KrishiConnect Demo”; use the source column to distinguish them.</p></div>
  </div>;
}
