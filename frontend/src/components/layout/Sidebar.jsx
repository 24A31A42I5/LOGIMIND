import { LayoutDashboard, Users, BrainCircuit, Package, History, Compass, BarChart3 } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useBusiness } from '../../context/useBusiness';

const icons = { 'Delivery Agents': Users, Shipments: Package, 'AI Analyzer': BrainCircuit, Memory: History, Expansion: Compass, Analytics: BarChart3 };

export default function Sidebar() {
  const { config } = useBusiness();
  const links = [{ to: '/dashboard', label: 'Dashboard' }, ...config.navigation];
  return (
    <aside className="hidden min-h-screen w-64 border-r border-slate-200 bg-slate-50 p-4 lg:flex lg:flex-col">
      <div className="mb-8 px-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">LOGIMIND</p>
        <h1 className="mt-2 text-xl font-bold text-slate-900">{config.label}</h1>
      </div>

      <nav className="space-y-2">
        {links.map(({ to, label }) => {
          const Icon = icons[label] || LayoutDashboard;
          return (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                isActive ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-900'
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
