import { Link } from "react-router-dom";
import { ArrowRight, BarChart3, BrainCircuit, MapPin, ShieldCheck, Sparkles, Activity } from "lucide-react";

export default function WelcomePage() {
  return (
    <div className="surface-grid min-h-screen overflow-hidden bg-[#f4f7fb] text-slate-900">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[#0b1220] text-white"><Activity size={20} /></div><span className="font-bold tracking-[0.18em]">LOGIMIND</span></div>
        <Link to="/login" className="text-sm font-semibold text-slate-600 hover:text-blue-700">Sign in <ArrowRight className="ml-1 inline" size={15} /></Link>
      </header>
      <div className="mx-auto grid min-h-[calc(100vh-88px)] max-w-7xl items-center gap-14 px-6 py-12 lg:grid-cols-[1.02fr_.98fr] lg:px-10 lg:py-20">
        <div>
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.16em] text-blue-700"><Sparkles size={14} /> Evidence-led intelligence</p>
          <h1 className="max-w-3xl text-5xl font-black leading-[1.05] tracking-tight text-slate-950 md:text-7xl">Know what is happening. <span className="text-blue-600">Act with confidence.</span></h1>
          <p className="mt-7 max-w-xl text-lg leading-8 text-slate-600">LOGIMIND brings real operational data, analytics, geospatial signals, AI reasoning, and institutional memory into one trusted command center.</p>
          <div className="mt-9 flex flex-col gap-3 sm:flex-row">
            <Link
              to="/signup"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-bold text-white shadow-xl shadow-blue-600/20 transition hover:bg-blue-700"
            >
              Create your workspace <ArrowRight size={17} />
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-bold text-slate-700 transition hover:border-slate-400 hover:bg-slate-50"
            >
              Sign in
            </Link>
          </div>
          <div className="mt-12 flex flex-wrap gap-x-6 gap-y-3 text-xs font-semibold text-slate-500"><span className="flex items-center gap-2"><ShieldCheck size={15} className="text-emerald-600" /> Tenant isolated</span><span className="flex items-center gap-2"><MapPin size={15} className="text-emerald-600" /> Real location data</span><span className="flex items-center gap-2"><BarChart3 size={15} className="text-emerald-600" /> Verified metrics</span></div>
        </div>
        <div className="relative">
          <div className="absolute -inset-8 rounded-[2.5rem] bg-blue-500/10 blur-3xl" />
          <div className="relative rounded-[2rem] border border-slate-200 bg-[#0b1220] p-4 shadow-2xl shadow-slate-900/20">
            <div className="rounded-2xl bg-[#111c32] p-5">
              <div className="flex items-center justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-slate-500">Live intelligence</p><p className="mt-1 text-lg font-bold text-white">Operations overview</p></div><span className="flex items-center gap-1.5 rounded-full bg-emerald-400/10 px-2.5 py-1 text-[10px] font-bold text-emerald-300"><span className="h-1.5 w-1.5 rounded-full bg-emerald-400" /> Connected</span></div>
              <div className="mt-5 grid grid-cols-3 gap-3">{[['On-time rate','—'],['Open actions','—'],['Evidence','Live']].map(([label,value]) => <div key={label} className="rounded-xl border border-white/10 bg-white/5 p-3"><p className="text-[10px] text-slate-500">{label}</p><p className="mt-2 text-xl font-bold text-white">{value}</p></div>)}</div>
              <div className="mt-4 rounded-xl border border-white/10 bg-white/5 p-4"><div className="flex items-end gap-2"><div className="h-16 w-1/6 rounded-t bg-blue-500/50" /><div className="h-24 w-1/6 rounded-t bg-blue-500/70" /><div className="h-20 w-1/6 rounded-t bg-blue-500/60" /><div className="h-32 w-1/6 rounded-t bg-emerald-400" /><div className="h-28 w-1/6 rounded-t bg-blue-500/80" /><div className="h-40 w-1/6 rounded-t bg-blue-400" /></div><div className="mt-3 flex justify-between text-[10px] text-slate-500"><span>Current evidence</span><span>By location</span></div></div>
              <div className="mt-4 flex items-center gap-3 rounded-xl border border-blue-400/20 bg-blue-500/10 p-3"><BrainCircuit className="text-blue-300" size={20} /><div><p className="text-xs font-bold text-white">AI reasoning grounded in your records</p><p className="mt-1 text-[10px] text-slate-400">No synthetic metrics. No invented outcomes.</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
