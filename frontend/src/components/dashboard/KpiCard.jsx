import { ArrowUpRight } from 'lucide-react';

export default function KpiCard({ label, value, trend, icon: Icon }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between text-slate-500">
        <span className="text-sm">{label}</span>
        {Icon && <Icon size={18} />}
      </div>
      <div className="mt-4 flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-slate-900">{value}</p>
        </div>
        <div className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-700">
          <ArrowUpRight size={12} />
          {trend}
        </div>
      </div>
    </div>
  );
}
