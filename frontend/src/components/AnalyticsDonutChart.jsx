export function AnalyticsDonutChart({ items }) {
  const total = items.reduce((sum, item) => sum + Number(item.value || 0), 0);
  let current = 0;
  const stops = items.map((item) => {
    const start = current;
    current += total ? (Number(item.value || 0) / total) * 100 : 0;
    return `${item.color} ${start}% ${current}%`;
  });
  const gradient = total ? `conic-gradient(${stops.join(', ')})` : 'conic-gradient(#e8ede6 0 100%)';

  return <div className="analytics-donut-layout">
    <div className="analytics-donut" style={{ '--donut-gradient': gradient }} role="img" aria-label={`Listing status breakdown: ${total} total`}>
      <div><strong>{total}</strong><span>listings</span></div>
    </div>
    <ul className="analytics-legend">{items.map((item) => <li key={item.label}><span className="analytics-legend__label"><i style={{ background: item.color }} />{item.label}</span><b>{item.value}</b></li>)}</ul>
  </div>;
}
