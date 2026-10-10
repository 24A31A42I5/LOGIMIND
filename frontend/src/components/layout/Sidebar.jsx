import { LayoutDashboard, Users, BrainCircuit, Package, History, Compass, BarChart3, Activity, ChevronRight } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useBusiness } from '../../context/useBusiness';

const icons = { 'Delivery Agents': Users, Shipments: Package, 'AI Analyzer': BrainCircuit, Memory: History, Expansion: Compass, Analytics: BarChart3 };

export default function Sidebar() {
  const { config } = useBusiness();
  const links = [{ to: '/dashboard', label: 'Dashboard' }, ...config.navigation];
  return (
    <aside className="hidden min-h-screen w-[272px] border-r border-slate-200/80 bg-[#0b1220] p-4 text-slate-300 lg:flex lg:flex-col">
      <div className="mb-10 px-3">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500 text-white shadow-lg shadow-blue-950/40"><Activity size={21} /></div>
          <div><p className="text-sm font-bold tracking-[0.18em] text-white">LOGIMIND</p><p className="mt-0.5 text-[10px] uppercase tracking-[0.16em] text-slate-500">Operational intelligence</p></div>
        </div>
        <div className="mt-8 rounded-xl border border-white/10 bg-white/5 p-3">
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-500">Active workspace</p>
          <h1 className="mt-1 text-sm font-semibold text-white">{config.label}</h1>
        </div>
      </div>

      <p className="px-3 pb-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">Workspace navigation</p>
      <nav className="space-y-1">
        {links.map(({ to, label }) => {
          const Icon = icons[label] || LayoutDashboard;
          return (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition ${
                isActive ? 'bg-blue-600 text-white shadow-lg shadow-blue-950/30' : 'text-slate-400 hover:bg-white/10 hover:text-white'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <Icon size={18} />
                {label}
                {isActive && <ChevronRight size={15} className="ml-auto opacity-70" />}
              </>
            )}
          </NavLink>
          );
        })}
      </nav>
      <div className="mt-auto rounded-xl border border-emerald-400/20 bg-emerald-400/10 p-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-300"><span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_#34d399]" />Data services connected</div>
        <p className="mt-2 text-[11px] leading-5 text-slate-500">Metrics are calculated from your operational records.</p>
      </div>
    </aside>
  );
}
