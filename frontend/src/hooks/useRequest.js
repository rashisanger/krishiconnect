import { useCallback, useEffect, useRef, useState } from 'react';

export function useRequest(loader, dependencies = []) {
  const [data, setData] = useState(null); const [loading, setLoading] = useState(true); const [error, setError] = useState('');
  const latestRequest = useRef(0);
  const reload = useCallback(async () => {
    const requestId = ++latestRequest.current;
    setLoading(true); setError('');
    try {
      const result = await loader();
      if (requestId === latestRequest.current) setData(result);
    } catch (err) {
      if (requestId === latestRequest.current) setError(err.message || 'Something went wrong.');
    } finally {
      if (requestId === latestRequest.current) setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies);
  useEffect(() => { reload(); }, [reload]);
  return { data, setData, loading, error, reload };
}
