const dayLabel = (value) => new Date(`${value}T00:00:00`).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });

export function PriceTrendChart({ points }) {
  const valid = points.filter((point) => point.average_modal_price != null);
  if (valid.length < 2) return <div className="analytics-empty">Price history will appear after more report dates are imported.</div>;

  const width = 680;
  const height = 220;
  const pad = { top: 18, right: 18, bottom: 34, left: 50 };
  const values = valid.map((point) => Number(point.average_modal_price));
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const x = (index) => pad.left + (index / (valid.length - 1)) * (width - pad.left - pad.right);
  const y = (value) => pad.top + ((max - value) / range) * (height - pad.top - pad.bottom);
  const line = valid.map((point, index) => `${index ? 'L' : 'M'} ${x(index)} ${y(Number(point.average_modal_price))}`).join(' ');
  const area = `${line} L ${x(valid.length - 1)} ${height - pad.bottom} L ${x(0)} ${height - pad.bottom} Z`;
  const mid = (min + max) / 2;

  return <div className="price-trend-chart">
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Average mandi modal price over recent report dates">
      {[min, mid, max].map((value, index) => <g key={index}>
        <line x1={pad.left} x2={width - pad.right} y1={y(value)} y2={y(value)} className="chart-gridline" />
        <text x={pad.left - 9} y={y(value) + 4} textAnchor="end" className="chart-axis-label">₹{Math.round(value).toLocaleString('en-IN')}</text>
      </g>)}
      <path d={area} className="price-trend-area" />
      <path d={line} className="price-trend-line" />
      {valid.map((point, index) => <g key={point.date}>
        <circle cx={x(index)} cy={y(Number(point.average_modal_price))} r="4" className="price-trend-point"><title>{dayLabel(point.date)}: ₹{Number(point.average_modal_price).toLocaleString('en-IN')}</title></circle>
        {(index === 0 || index === valid.length - 1 || index === Math.floor((valid.length - 1) / 2)) && <text x={x(index)} y={height - 10} textAnchor="middle" className="chart-axis-label">{dayLabel(point.date)}</text>}
      </g>)}
    </svg>
    <p className="chart-caption">Daily average modal price across saved market records · ₹ per quintal</p>
  </div>;
}
