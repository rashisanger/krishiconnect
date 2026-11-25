import { useState } from 'react';
import { ArrowRight, ArrowUpRight, BarChart3, CircleDollarSign, Database, RefreshCw, ShieldCheck, Store, Users } from 'lucide-react';
import { Link } from 'react-router-dom';
import { analyticsApi, marketApi } from '../api/services.js';
import { unwrapPage } from '../api/client.js';
import { useRequest } from '../hooks/useRequest.js';
import { DJANGO_ADMIN_URL } from '../api/client.js';
import { EmptyState, ErrorState, LoadingState, Notice } from '../components/Feedback.jsx';
import { FormField } from '../components/FormField.jsx';
import { StatCard } from '../components/StatCard.jsx';
import { AnalyticsColumnChart } from '../components/AnalyticsColumnChart.jsx';
import { AnalyticsDonutChart } from '../components/AnalyticsDonutChart.jsx';
import { PriceTrendChart } from '../components/PriceTrendChart.jsx';

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value || 0));
const formatDate = (value) => value ? new Date(value).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : 'No data yet';

export function AdminDashboardPage() {
  const [refreshing, setRefreshing] = useState(false);
  const [filters, setFilters] = useState({ crop: '', state: '', district: '', mandi: '' });
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const dashboard = useRequest(async () => {
    const [overview, prices, cropAverages] = await Promise.all([
      analyticsApi.overview(), marketApi.prices({ limit: 6 }), analyticsApi.cropAveragePrices(),
    ]);
    return { overview, prices: unwrapPage(prices), priceCount: prices.count, cropAverages: cropAverages.results || [] };
  }, []);
  const data = dashboard.data;
  const latestDate = data?.prices?.reduce((latest, row) => !latest || row.price_date > latest ? row.price_date : latest, null);
  const cropPriceItems = (data?.cropAverages || []).slice(0, 6).map((item) => ({
    label: item.crop_name,
    value: item.average_modal_price,
  }));
  const tradeStatusItems = [
    { label: 'Open enquiries', value: data?.overview?.enquiries?.open || 0, color: '#d19a43' },
    { label: 'Responded enquiries', value: data?.overview?.enquiries?.responded || 0, color: '#568a5e' },
    { label: 'Accepted enquiries', value: data?.overview?.enquiries?.accepted || 0, color: '#326d43' },
    { label: 'Pending offers', value: data?.overview?.offers?.pending || 0, color: '#66819b' },
    { label: 'Accepted offers', value: data?.overview?.offers?.accepted || 0, color: '#8b70a8' },
  ];
  const listingStatusItems = [
    { label: 'Available', value: data?.overview?.listings?.available || 0, color: '#4d8052' },
    { label: 'Reserved', value: data?.overview?.listings?.reserved || 0, color: '#d19a43' },
    { label: 'Sold', value: data?.overview?.listings?.sold || 0, color: '#66819b' },
    { label: 'Inactive', value: data?.overview?.listings?.inactive || 0, color: '#9ba69a' },
  ];

  async function refreshMarketData(event) {
    event.preventDefault(); setRefreshing(true); setError(''); setNotice('');
    const submittedFilters = Object.fromEntries(Object.entries(filters).filter(([, value]) => value.trim()));
    try {
      const result = await marketApi.refresh({ ...submittedFilters, limit: 100 });
      setNotice(`Refresh complete: ${result.created} new, ${result.updated} updated, ${result.skipped} skipped.`);
      await dashboard.reload();
    } catch (err) { setError(err.message); }
    finally { setRefreshing(false); }
  }

  return <div className="admin-dashboard">
    <div className="welcome-row"><div><span className="eyebrow">KRISHICONNECT ADMINISTRATION</span><h1>Platform overview <ShieldCheck className="admin-shield" size={23} /></h1><p>Keep an eye on marketplace activity and the freshness of reported mandi data.</p></div><a className="button button--secondary" href={DJANGO_ADMIN_URL} target="_blank" rel="noreferrer">Open Django Admin <ArrowUpRight size={15} /></a></div>
    {dashboard.loading ? <LoadingState label="Gathering platform activity…" /> : dashboard.error ? <ErrorState message={dashboard.error} onRetry={dashboard.reload} /> : <>
      <section className="stat-grid admin-stat-grid">
        <StatCard icon={Store} label="Available listings" value={data?.overview?.total_available_crop_listings ?? 0} detail="Currently open to buyers" />
        <StatCard icon={Users} label="Registered farmers" value={data?.overview?.total_registered_farmers ?? 0} detail="Farmer profiles on platform" />
        <StatCard icon={Users} label="Registered buyers" value={data?.overview?.total_registered_buyers ?? 0} detail="Buyer profiles on platform" />
        <StatCard icon={CircleDollarSign} label="Open enquiries" value={data?.overview?.enquiries?.open ?? 0} detail={`${data?.overview?.enquiries?.total ?? 0} total conversations`} />
      </section>
      <section className="admin-dashboard-grid">
        <div className="panel admin-sync-panel"><div className="panel__heading"><div><span className="eyebrow">AGMARKNET DATA</span><h2>Refresh market prices</h2></div><span className="admin-sync-icon"><RefreshCw size={18} /></span></div><p className="admin-panel-intro">Searches use the latest records saved in KrishiConnect. Refresh from the Government of India data API to bring in newer reports for a crop or location.</p><Notice>{notice}</Notice><Notice tone="danger">{error}</Notice><form className="admin-refresh-form" onSubmit={refreshMarketData}><div className="form-grid"><FormField label="Crop" name="crop" value={filters.crop} onChange={(e) => setFilters({ ...filters, crop: e.target.value })} placeholder="Optional, e.g. Onion" /><FormField label="State" name="state" value={filters.state} onChange={(e) => setFilters({ ...filters, state: e.target.value })} placeholder="Optional" /><FormField label="District" name="district" value={filters.district} onChange={(e) => setFilters({ ...filters, district: e.target.value })} placeholder="Optional" /><FormField label="Mandi" name="mandi" value={filters.mandi} onChange={(e) => setFilters({ ...filters, mandi: e.target.value })} placeholder="Optional" /></div><div className="admin-refresh-footer"><span>Up to 100 matching source records per refresh.</span><button className="button button--primary" disabled={refreshing}>{refreshing ? <><RefreshCw className="spin" size={15} /> Refreshing…</> : <><RefreshCw size={15} /> Refresh data</>}</button></div></form></div>
        <aside className="admin-side-column"><div className="market-note admin-freshness-card"><div className="market-note__icon"><Database size={18} /></div><div><small>LOCAL MARKET DATA</small><h3>{data?.priceCount ?? 0} price records</h3><p>Most recent report date in this database: <b>{formatDate(latestDate)}</b>.</p><Link to="/market">Open price search <ArrowRight size={14} /></Link></div></div><div className="panel admin-status-panel"><div className="panel__heading"><div><span className="eyebrow">PLATFORM HEALTH</span><h2>Trade activity</h2></div><BarChart3 size={18} color="#638558" /></div><div className="admin-status-row"><span>Enquiries responded</span><b>{data?.overview?.enquiries?.responded ?? 0}</b></div><div className="admin-status-row"><span>Offers awaiting a decision</span><b>{data?.overview?.offers?.pending ?? 0}</b></div><div className="admin-status-row"><span>Accepted offers</span><b>{data?.overview?.offers?.accepted ?? 0}</b></div></div></aside>
      </section>
      <section className="admin-analytics-grid">
        <article className="panel analytics-panel analytics-panel--wide"><div className="panel__heading"><div><span className="eyebrow">MARKET MOVEMENT</span><h2>Recent modal price trend</h2></div><span className="analytics-period">Last 14 report dates</span></div><PriceTrendChart points={data?.overview?.market_price_trend || []} /></article>
        <article className="panel analytics-panel"><div className="panel__heading"><div><span className="eyebrow">PRICE LANDSCAPE</span><h2>Average price by crop</h2></div></div><AnalyticsColumnChart items={cropPriceItems} emptyLabel="Import market records to compare crops." formatValue={(value) => money(value)} /></article>
        <article className="panel analytics-panel"><div className="panel__heading"><div><span className="eyebrow">MARKETPLACE INVENTORY</span><h2>Listing availability</h2></div></div><AnalyticsDonutChart items={listingStatusItems} /></article>
        <article className="panel analytics-panel analytics-panel--wide"><div className="panel__heading"><div><span className="eyebrow">BUYER–FARMER ACTIVITY</span><h2>Enquiries and offers</h2></div><span className="analytics-period">Current status totals</span></div><AnalyticsColumnChart items={tradeStatusItems} formatValue={(value) => Math.round(value).toLocaleString('en-IN')} /></article>
      </section>
      <section className="panel admin-prices-panel"><div className="panel__heading"><div><span className="eyebrow">MOST RECENTLY REPORTED</span><h2>Market price records</h2></div><Link className="panel__link" to="/market">Search all prices <ArrowRight size={15} /></Link></div>{data?.prices?.length ? <div className="market-table-wrap"><table className="market-table"><thead><tr><th>Crop</th><th>Market</th><th>State & district</th><th>Modal price</th><th>Report date</th><th>Source</th></tr></thead><tbody>{data.prices.map((row) => <tr key={row.id}><td><b>{row.crop_name}</b></td><td>{row.mandi}</td><td>{row.district}, {row.state}</td><td><strong className="modal-price">{money(row.modal_price)}</strong></td><td>{formatDate(row.price_date)}</td><td>{row.source}</td></tr>)}</tbody></table></div> : <EmptyState title="No market data yet" message="Use the refresh form above or import records from the management command." />}</section>
    </>}
  </div>;
}
