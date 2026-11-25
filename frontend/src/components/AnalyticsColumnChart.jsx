const palette = ['#4d8052', '#86a66f', '#d0a04e', '#7892a4', '#9479a7', '#bf7f5e'];

export function AnalyticsColumnChart({ items, emptyLabel = 'No data available', formatValue = (value) => value }) {
  if (!items.length) return <div className="analytics-empty">{emptyLabel}</div>;
  const width = 680;
  const height = 270;
  const pad = { top: 30, right: 16, bottom: 55, left: 48 };
  const values = items.map((item) => Number(item.value) || 0);
  const maxValue = Math.max(...values, 1);
  const plotHeight = height - pad.top - pad.bottom;
  const plotWidth = width - pad.left - pad.right;
  const slot = plotWidth / items.length;
  const barWidth = Math.min(54, slot * 0.55);
  const ticks = [0, maxValue / 2, maxValue];

  return <div className="analytics-column-chart">
    <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Bar chart">
      {ticks.map((tick, index) => {
        const y = pad.top + plotHeight - (tick / maxValue) * plotHeight;
        return <g key={index}><line x1={pad.left} x2={width - pad.right} y1={y} y2={y} className="chart-gridline" /><text x={pad.left - 8} y={y + 4} textAnchor="end" className="chart-axis-label">{formatValue(tick, true)}</text></g>;
      })}
      {items.map((item, index) => {
        const value = Number(item.value) || 0;
        const barHeight = (value / maxValue) * plotHeight;
        const barX = pad.left + slot * index + (slot - barWidth) / 2;
        const barY = pad.top + plotHeight - barHeight;
        const center = barX + barWidth / 2;
        return <g key={item.label}>
          <rect x={barX} y={barY} width={barWidth} height={Math.max(value ? 3 : 0, barHeight)} rx="6" fill={item.color || palette[index % palette.length]} className="analytics-column" />
          <text x={center} y={Math.max(pad.top - 4, barY - 8)} textAnchor="middle" className="chart-value-label">{formatValue(value)}</text>
          <text x={center} y={height - 27} textAnchor="middle" className="chart-category-label">{item.label.length > 13 ? `${item.label.slice(0, 12)}…` : item.label}</text>
          <title>{item.label}: {formatValue(value)}</title>
        </g>;
      })}
    </svg>
  </div>;
}
