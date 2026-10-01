import { useEffect, useState } from 'react';
import api from '../../api/client';
import { useBusiness } from '../../context/useBusiness';

export default function DomainRecordsPage({ title, description, endpoint, columns }) {
  const { config } = useBusiness();
  const [records, setRecords] = useState([]);
  const [synthetic, setSynthetic] = useState(false);
  const [state, setState] = useState('loading');

  useEffect(() => {
    api.get(endpoint).then(({ data }) => { setRecords(data.records || []); setSynthetic(Boolean(data.synthetic)); setState('ready'); }).catch(() => setState('error'));
  }, [endpoint]);

  if (state === 'loading') return <p className="text-slate-600">Loading {title.toLowerCase()}...</p>;
  if (state === 'error') return <p className="rounded-lg bg-amber-50 p-4 text-amber-800">{title} data is unavailable. Connect domain records to activate this workspace.</p>;
  return <div className="space-y-5"><div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">{config.label}</p><h1 className="mt-1 text-3xl font-bold text-slate-900">{title}</h1><p className="mt-2 text-slate-600">{description}</p></div>{synthetic && <p className="rounded-lg bg-slate-200 px-3 py-2 text-sm text-slate-700">Synthetic demo data. Replace with connected operational records for live evidence.</p>}<div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm"><table className="min-w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500"><tr>{columns.map((column) => <th key={column.key} className="px-4 py-3">{column.label}</th>)}</tr></thead><tbody className="divide-y divide-slate-100">{records.map((record, index) => <tr key={record.id || record.order_id || record.sale_id || record.booking_id || record.shipment_id || index}>{columns.map((column) => <td key={column.key} className="whitespace-nowrap px-4 py-3 text-slate-700">{record[column.key] ?? '-'}</td>)}</tr>)}</tbody></table>{records.length === 0 && <p className="p-6 text-slate-600">No {title.toLowerCase()} records are available.</p>}</div></div>;
}