import { useEffect, useState } from 'react';

export default function DomainRecordsPage({ title, description, loadRecords, recordLabel, fields }) {
  const [records, setRecords] = useState([]);
  const [state, setState] = useState('loading');
  useEffect(() => { loadRecords().then((response) => { setRecords(response.data.records || []); setState('ready'); }).catch(() => setState('error')); }, [loadRecords]);
  if (state === 'loading') return <p className="text-slate-600">Loading {recordLabel.toLowerCase()}...</p>;
  if (state === 'error') return <p className="rounded-lg bg-amber-50 p-4 text-amber-800">{recordLabel} data is unavailable.</p>;
  return <div className="space-y-5"><div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">Current data</p><h1 className="mt-1 text-3xl font-bold text-slate-900">{title}</h1><p className="mt-2 text-slate-600">{description}</p></div><p className="rounded-lg bg-slate-200 px-3 py-2 text-sm text-slate-700">Synthetic demo data. Connect MongoDB operational records to replace it.</p><div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm"><table className="min-w-full text-left text-sm"><thead className="border-b border-slate-200 bg-slate-50 text-slate-500"><tr>{fields.map((field) => <th key={field.key} className="px-4 py-3 font-semibold">{field.label}</th>)}</tr></thead><tbody>{records.map((record) => <tr key={record.order_id || record.sale_id || record.booking_id || record.shipment_id} className="border-b border-slate-100 last:border-0">{fields.map((field) => <td key={field.key} className="px-4 py-3 text-slate-700">{record[field.key] ?? '-'}</td>)}</tr>)}</tbody></table></div></div>;
}