import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import DemoToolbar from './DemoToolbar';

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/delivery-agents', label: 'Delivery Agents' },
  { to: '/ai-analyzer', label: 'AI Analyzer' },
  { to: '/shipments', label: 'Shipments' },
  { to: '/memory', label: 'Memory' },
];

export default function Shell() {
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen">
        <Sidebar />

        <div className="flex-1">
          <header className="border-b border-slate-200 bg-white px-4 py-3 shadow-sm lg:hidden">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">LOGIMIND</p>
              </div>
              <button type="button" onClick={() => setOpen((value) => !value)} className="rounded-lg border border-slate-200 p-2">
                {open ? <X size={18} /> : <Menu size={18} />}
              </button>
            </div>
            {open && (
              <nav className="mt-4 space-y-2">
                {navItems.map(({ to, label }) => (
                  <NavLink key={to} to={to} onClick={() => setOpen(false)} className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm font-medium ${isActive ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-700'}`}>
                    {label}
                  </NavLink>
                ))}
              </nav>
            )}
          </header>
          <DemoToolbar />

          <main className="p-4 md:p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
