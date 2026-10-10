import { ArrowUpRight } from 'lucide-react';

export default function KpiCard({ label, value, trend, icon: Icon }) {
  return (
    <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-[0_8px_30px_rgba(15,23,42,.04)] transition hover:-translate-y-0.5 hover:shadow-lg">
      <div className="flex items-center justify-between text-slate-500">
        <span className="text-xs font-semibold uppercase tracking-wide">{label}</span>
        {Icon && <span className="rounded-lg bg-blue-50 p-2 text-blue-600"><Icon size={17} /></span>}
      </div>
      <div className="mt-4 flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-slate-900">{value}</p>
        </div>
        <div className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700">
          <ArrowUpRight size={12} />
          {trend}
        </div>
      </div>
    </div>
  );
}
