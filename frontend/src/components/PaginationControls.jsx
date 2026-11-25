import { ChevronLeft, ChevronRight } from 'lucide-react';
import { pageRange } from '../utils/pagination.js';

export function PaginationControls({ page, count, pageSize = 5, hasPrevious, hasNext, onChange }) {
  if (!count || (!hasPrevious && !hasNext)) return null;
  const { first, last } = pageRange(page, count, pageSize);
  return <nav className="pagination-controls" aria-label="Pagination">
    <span>Showing {first}–{last} of {count}</span>
    <div>
      <button type="button" className="button button--secondary button--small" onClick={() => onChange(page - 1)} disabled={!hasPrevious} aria-label="Previous page"><ChevronLeft size={15} /> Previous</button>
      <span className="pagination-page">Page {page}</span>
      <button type="button" className="button button--secondary button--small" onClick={() => onChange(page + 1)} disabled={!hasNext} aria-label="Next page">Next <ChevronRight size={15} /></button>
    </div>
  </nav>;
}
