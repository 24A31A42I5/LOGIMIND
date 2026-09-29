import { LayoutDashboard, Users, BrainCircuit, Package, History } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/delivery-agents', label: 'Delivery Agents', icon: Users },
  { to: '/ai-analyzer', label: 'AI Analyzer', icon: BrainCircuit },
  { to: '/shipments', label: 'Shipments', icon: Package },
  { to: '/memory', label: 'Memory', icon: History },
];

export default function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-64 border-r border-slate-200 bg-slate-50 p-4 lg:flex lg:flex-col">
      <div className="mb-8 px-2">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">LOGIMIND</p>
        <h1 className="mt-2 text-xl font-bold text-slate-900">Distributor</h1>
      </div>

      <nav className="space-y-2">
        {links.map(({ to, label, icon: Icon }) => (
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
        ))}
      </nav>
    </aside>
  );
}
