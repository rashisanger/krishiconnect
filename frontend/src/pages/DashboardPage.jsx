import { ArrowRight, Bell, CircleDollarSign, MapPin, PackageOpen, Sprout, Store } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../state/AuthContext.jsx';
import { useRequest } from '../hooks/useRequest.js';
import { analyticsApi, listingApi, marketApi, negotiationApi } from '../api/services.js';
import { unwrapPage } from '../api/client.js';
import { ErrorState, LoadingState, EmptyState } from '../components/Feedback.jsx';
import { StatCard } from '../components/StatCard.jsx';

const money = (value) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value || 0));
const date = (value) => value ? new Date(value).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : '—';

export function DashboardPage() {
  const { user } = useAuth(); const farmer = user?.role === 'FARMER';
  const feed = useRequest(async () => {
    const results = farmer ? await Promise.allSettled([listingApi.mine({ limit: 5 }), analyticsApi.farmerListings(), negotiationApi.farmerEnquiries({ limit: 4 }), negotiationApi.farmerOffers({ limit: 4 }), marketApi.prices({ limit: 4 })])
      : await Promise.allSettled([listingApi.browse({ limit: 4 }), negotiationApi.buyerEnquiries({ limit: 4 }), negotiationApi.buyerOffers({ limit: 4 }), marketApi.prices({ limit: 4 })]);
    const ok = (index, fallback = null) => results[index].status === 'fulfilled' ? results[index].value : fallback;
    return farmer ? { listings: unwrapPage(ok(0, {})), analytics: ok(1), enquiries: unwrapPage(ok(2, {})), offers: unwrapPage(ok(3, {})), prices: unwrapPage(ok(4, {})) }
      : { listings: unwrapPage(ok(0, {})), enquiries: unwrapPage(ok(1, {})), offers: unwrapPage(ok(2, {})), prices: unwrapPage(ok(3, {})) };
  }, [farmer]);
  const data = feed.data;
  const greeting = new Date().getHours() < 12 ? 'Good morning' : new Date().getHours() < 17 ? 'Good afternoon' : 'Good evening';
  return <div className="dashboard-page"><div className="welcome-row"><div><span className="eyebrow">YOUR KRISHICONNECT WORKSPACE</span><h1>{greeting}, {user?.first_name || user?.username}<span className="greeting-sun">☀</span></h1><p>{farmer ? 'Here’s what’s happening with your harvest today.' : 'Your next good partnership could be just around the corner.'}</p></div><div className="welcome-row__date">{new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long' })}<span><span className="live-dot" /> Your market, at a glance</span></div></div>
    {feed.loading ? <LoadingState label="Gathering your latest activity…" /> : feed.error ? <ErrorState message={feed.error} onRetry={feed.reload} /> : <>
      <section className="stat-grid">{farmer ? <><StatCard icon={PackageOpen} label="My listings" value={data?.analytics?.listing_statistics?.total ?? data?.listings?.length ?? '—'} detail={`${data?.analytics?.listing_statistics?.available ?? 0} available now`} /><StatCard icon={Bell} label="New enquiries" value={data?.enquiries?.filter((item) => item.status === 'OPEN').length ?? 0} detail="Waiting for your reply" /><StatCard icon={CircleDollarSign} label="Offers received" value={data?.offers?.filter((item) => item.status === 'PENDING').length ?? 0} detail="Ready for your review" /></> : <><StatCard icon={Store} label="Fresh listings" value={data?.listings?.length ?? 0} detail="Available from local growers" /><StatCard icon={Bell} label="My enquiries" value={data?.enquiries?.length ?? 0} detail="Conversations in progress" /><StatCard icon={CircleDollarSign} label="Offers made" value={data?.offers?.length ?? 0} detail="Your buying activity" /></>}</section>
      <section className="dashboard-grid"><div className="panel panel--listings"><div className="panel__heading"><div><span className="eyebrow">{farmer ? 'YOUR HARVEST' : 'FROM THE COMMUNITY'}</span><h2>{farmer ? 'Recent crop listings' : 'Freshly listed crops'}</h2></div><Link className="panel__link" to="/listings">{farmer ? 'Manage listings' : 'Explore all'} <ArrowRight size={15} /></Link></div>{data?.listings?.length ? <div className="mini-list">{data.listings.slice(0, 4).map((item) => <article className="mini-listing" key={item.id}><span className="crop-avatar"><Sprout size={19} /></span><div className="mini-listing__name"><b>{item.crop_name || 'Crop listing'}</b><small><MapPin size={12} /> {item.district}, {item.state}</small></div><div className="mini-listing__quantity"><b>{Number(item.quantity).toLocaleString('en-IN')} <small>{item.unit}</small></b><small>available</small></div><div className="mini-listing__price">{money(item.expected_price)}<small>per unit</small></div></article>)}</div> : <EmptyState title={farmer ? 'Your first listing starts here' : 'No crops listed just yet'} message={farmer ? 'Let buyers know what you’re growing and when it’s ready.' : 'Check back soon as local farmers share their harvest.'} action={farmer ? <Link className="button button--primary button--small" to="/listings">Add a crop <ArrowRight size={14} /></Link> : null} />}</div>
        <aside className="dashboard-side"><div className="market-note"><div className="market-note__icon"><CircleDollarSign size={18} /></div><div><small>MARKET WATCH</small><h3>Prices worth knowing</h3><p>Keep an eye on the latest mandi prices before your next conversation.</p><Link to="/market">Explore market prices <ArrowRight size={14} /></Link></div></div><div className="panel activity-panel"><div className="panel__heading"><div><span className="eyebrow">THE LATEST</span><h2>Market activity</h2></div><Link className="panel__link" to="/market">See all</Link></div>{data?.prices?.slice(0, 3).map((price) => <div className="price-row" key={price.id}><span className="price-row__leaf"><Sprout size={16} /></span><span><b>{price.crop_name}</b><small>{price.mandi}, {price.state}</small></span><span className="price-row__value"><b>{money(price.modal_price)}</b><small>{date(price.price_date)}</small></span></div>)}{!data?.prices?.length && <p className="subtle-text">Market prices will appear here when data is available.</p>}</div></aside></section>
    </>}
  </div>;
}
