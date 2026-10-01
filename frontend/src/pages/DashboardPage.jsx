import { useEffect, useState } from 'react';
import api from '../api/client';
import { getOverallAnalytics } from '../api/analytics';
import { getShipments } from '../api/shipments';
import { getAgents } from '../api/agents';
import OperationsMap from '../components/map/OperationsMap';
import KpiCard from '../components/dashboard/KpiCard';
import TodayDeliveriesTable from '../components/dashboard/TodayDeliveriesTable';
import { Users, Truck, Clock3, AlertTriangle } from 'lucide-react';
import ActiveAgentsModal from '../components/dashboard/ActiveAgentsModal';
import Badge from '../components/common/Badge';
import { useBusiness } from '../context/useBusiness';

function DomainDashboard({ config }) {
  const [records, setRecords] = useState([]);
  const [synthetic, setSynthetic] = useState(false);
  const [state, setState] = useState('loading');

  useEffect(() => {
    api.get(config.operationalEndpoint).then(({ data }) => {
      setRecords(data.records || []);
      setSynthetic(Boolean(data.synthetic));
      setState('ready');
    }).catch(() => setState('error'));
  }, [config.operationalEndpoint]);

  if (state === 'loading') return <div className="p-6 text-slate-600">Loading {config.label.toLowerCase()} operations...</div>;
  if (state === 'error') return <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-800">{config.label} operational data is unavailable.</div>;
  const values = [records.length, records.reduce((sum, record) => sum + Number(record.sales || record.volume || record.units || record.demand || 0), 0), new Set(records.map((record) => record.location)).size, records.reduce((sum, record) => sum + Number(record.demand || 0), 0)];
  return <div className="space-y-6"><div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">{config.label} workspace</p><h1 className="mt-1 text-3xl font-bold text-slate-900">Current operations</h1><p className="mt-2 text-slate-600">Business-specific signals for demand, performance, and expansion readiness.</p></div>{synthetic && <p className="rounded-lg bg-slate-200 px-3 py-2 text-sm text-slate-700">Synthetic demo data. These values are representative, not external evidence.</p>}<div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{config.metrics.map((metric, index) => <div key={metric} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm text-slate-500">{metric}</p><p className="mt-3 text-3xl font-bold text-slate-900">{values[index] ?? 0}</p><p className="mt-2 text-sm text-slate-600">Current operating signal</p></div>)}</div></div>;
}

export default function DashboardPage() {
  const { profile, config } = useBusiness();
  const [overall, setOverall] = useState(null);
  const [shipments, setShipments] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAgents, setShowAgents] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const [overallRes, shipmentsRes, agentsRes] = await Promise.all([
          getOverallAnalytics(),
          getShipments(),
          getAgents(),
        ]);
        setOverall(overallRes.data);
        setShipments(shipmentsRes.data);
        setAgents(agentsRes.data);
      } catch {
        setError('Dashboard data is unavailable. Check the backend connection and try again.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (profile?.businessType && profile.businessType !== 'distributor') return <DomainDashboard config={config} />;

  if (loading) return <div className="p-6 text-slate-600">Loading dashboard...</div>;
  if (error) return <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-800">{error}</div>;

  const metrics = [
    { label: 'Packages Received', value: overall?.total_deliveries ?? 0, trend: '+8.4%', icon: Truck },
    { label: 'Dispatched', value: '482', trend: '+6.2%', icon: Truck },
    { label: 'Delivered', value: '402', trend: '+7.1%', icon: Clock3 },
    { label: 'Out for Delivery', value: '61', trend: '-2.1%', icon: Users },
    { label: 'Delayed', value: '17', trend: 'Needs review', icon: AlertTriangle },
    { label: 'Failed', value: '6', trend: '1 critical', icon: AlertTriangle },
    { label: 'Avg Delivery Time', value: `${overall?.average_delivery_time ?? 0} min`, trend: '-5 min', icon: Clock3 },
    { label: 'Active Delivery Agents', value: overall?.active_agents ?? 0, trend: 'Live', icon: Users, onClick: () => setShowAgents(true) },
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map(({ label, value, trend, icon: Icon, onClick }) => (
          <button key={label} type="button" onClick={onClick} className="text-left" disabled={!onClick}>
            <KpiCard label={label} value={value} trend={trend} icon={Icon} />
          </button>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Operational Map</h2>
            <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-700">Live view</span>
          </div>
          <OperationsMap areaData={overall?.area_hotspots ?? []} />
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-lg font-semibold text-slate-900">Active agents</h3>
          <div className="space-y-3">
            {agents.slice(0, 5).map((agent) => (
              <div key={agent.agent_id} className="rounded-xl border border-slate-200 p-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-800">{agent.agent_id}</span>
                  <Badge tone={agent.status === 'Delayed' ? 'warning' : 'info'}>{agent.status}</Badge>
                </div>
                <p className="mt-2 text-sm text-slate-600">Today&apos;s deliveries: {agent.today_deliveries}</p>
                <p className="text-sm text-slate-600">Completed: {agent.completed} · Delayed: {agent.delayed}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <TodayDeliveriesTable shipments={shipments.slice(0, 8)} />
      </div>
      {showAgents && <ActiveAgentsModal agents={agents} onClose={() => setShowAgents(false)} />}
    </div>
  );
}
