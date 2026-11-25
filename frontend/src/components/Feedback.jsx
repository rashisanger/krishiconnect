import { AlertCircle, LoaderCircle, RefreshCw } from 'lucide-react';

export function LoadingState({ label = 'Getting things ready…' }) { return <div className="state-panel" role="status"><LoaderCircle className="spin" size={24} /><span>{label}</span></div>; }
export function ErrorState({ message, onRetry }) { return <div className="state-panel state-panel--error" role="alert"><AlertCircle size={21} /><span>{message}</span>{onRetry && <button className="icon-button" onClick={onRetry} aria-label="Try again"><RefreshCw size={16} /></button>}</div>; }
export function EmptyState({ title, message, action }) { return <div className="empty-state"><span className="empty-state__icon">✳</span><h3>{title}</h3><p>{message}</p>{action}</div>; }
export function Notice({ children, tone = 'success' }) { return children ? <div className={`notice notice--${tone}`} role={tone === 'danger' ? 'alert' : 'status'}>{children}</div> : null; }
