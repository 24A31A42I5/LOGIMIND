import { useCallback, useEffect, useState } from "react";
import api from "../api/client";
import { getOverallAnalytics } from "../api/analytics";
import { getShipments } from "../api/shipments";
import { getAgentLocations, getAgents } from "../api/agents";
import OperationsMap from "../components/map/OperationsMap";
import KpiCard from "../components/dashboard/KpiCard";
import TodayDeliveriesTable from "../components/dashboard/TodayDeliveriesTable";
import {
  Users,
  Truck,
  Clock3,
  AlertTriangle,
  RefreshCw,
  Database,
  ArrowUpRight,
  ChevronRight,
  CircleAlert,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import ActiveAgentsModal from "../components/dashboard/ActiveAgentsModal";
import Badge from "../components/common/Badge";
import { useBusiness } from "../context/useBusiness";

function DomainDashboard({ config, profile }) {
  const [records, setRecords] = useState([]);
  const [state, setState] = useState("loading");
  const [overall, setOverall] = useState(null);
  const [period, setPeriod] = useState("overall");
  const [lastUpdated, setLastUpdated] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadDashboard = useCallback(async (showSpinner = true) => {
    if (showSpinner) setRefreshing(true);
    try {
      const [{ data: operations }, { data: analytics }] = await Promise.all([
        api.get(config.operationalEndpoint),
        getOverallAnalytics({ period }),
      ]);
      setRecords(operations.records || []);
      setOverall(analytics);
      setLastUpdated(new Date());
      setState("ready");
    } catch {
      setState("error");
    } finally {
      setRefreshing(false);
    }
  }, [config.operationalEndpoint, period]);

  useEffect(() => {
    const initialLoad = window.setTimeout(() => {
      void loadDashboard(false);
    }, 0);
    return () => window.clearTimeout(initialLoad);
  }, [loadDashboard]);

  /* Keep the command center current without inventing values. */
  useEffect(() => {
    const interval = window.setInterval(() => void loadDashboard(false), 60000);
    return () => window.clearInterval(interval);
  }, [loadDashboard]);

  if (state === "loading")
    return (
      <div className="flex min-h-[60vh] items-center justify-center text-slate-600">
        Loading {config.label.toLowerCase()} operations...
      </div>
    );
  if (state === "error")
    return (
      <div className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-800">
        <div className="flex items-center gap-3 font-semibold"><CircleAlert size={19} /> {config.label} operational data is unavailable.</div>
        <button type="button" onClick={() => loadDashboard()} className="mt-4 rounded-lg bg-rose-700 px-4 py-2 text-sm font-semibold text-white">Retry connection</button>
      </div>
    );
  const domainMetrics = overall?.domain_metrics || {};
  const valuesByDomain = {
    restaurant: [
      domainMetrics.orders,
      domainMetrics.average_preparation_minutes,
      domainMetrics.revenue,
      domainMetrics.food_cost_percentage,
    ],
    retail: [
      domainMetrics.revenue,
      domainMetrics.transactions,
      domainMetrics.units_sold,
      domainMetrics.gross_margin_percentage,
    ],
    raw_material: [
      domainMetrics.open_orders,
      domainMetrics.available_stock,
      domainMetrics.supplier_on_time_rate,
      domainMetrics.average_lead_time_days,
    ],
    service_provider: [
      domainMetrics.open_work_orders,
      domainMetrics.completed_work_orders,
      domainMetrics.average_resolution_hours,
      domainMetrics.sla_compliance_rate,
    ],
  };
  const values = valuesByDomain[config.id] || [
    overall?.total_deliveries,
    overall?.delay_rate,
    overall?.average_delivery_time,
    overall?.failed_delivery_rate,
  ];
  const locations = overall?.area_hotspots || overall?.hotspots || [];
  const chartData = locations.map((item) => ({
    name: item.location || item.area || item.name,
    records: item.volume ?? item.record_count ?? item.deliveries ?? 0,
    demand: item.demand,
  }));
  const formatValue = (value) =>
    value === null || value === undefined ? "—" : value;
  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-end">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-blue-700">{config.label} command center</p>
          <h1 className="mt-2 text-4xl font-black tracking-tight text-slate-950">Operational control room</h1>
          <p className="mt-2 max-w-2xl text-slate-600">Verified signals, emerging pressure points, and the next operational decisions for your business.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <select value={period} onChange={(event) => setPeriod(event.target.value)} className="rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-sm font-semibold text-slate-700 shadow-sm">
            <option value="today">Today</option><option value="week">Last 7 days</option><option value="month">Last 30 days</option><option value="overall">All available data</option>
          </select>
          <button type="button" onClick={() => loadDashboard()} disabled={refreshing} className="inline-flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-60"><RefreshCw size={16} className={refreshing ? "animate-spin" : ""} /> Refresh</button>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-xs text-slate-500 shadow-sm">
        <span className="flex items-center gap-2 font-semibold text-emerald-700"><Database size={15} /> MongoDB operational records <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" /></span>
        <span>{records.length ? `${records.length} records in selected window` : "No records in selected window"} {lastUpdated && ` · Updated ${lastUpdated.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`}</span>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {config.metrics.map((metric, index) => (
          <div
            key={metric}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <p className="text-sm text-slate-500">{metric}</p>
            <p className="mt-3 text-3xl font-bold text-slate-900">
              {formatValue(values[index])}
            </p>
            <p className="mt-2 text-xs font-medium text-slate-500">{records.length ? "Observed in selected period" : "Awaiting operational data"}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h2 className="mb-3 text-lg font-semibold text-slate-900">
            {config.label} operating evidence
          </h2>
          {chartData.length ? (
            <div className="h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="records" fill="#2563eb" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="demand" fill="#14b8a6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex h-[260px] items-center justify-center rounded-xl border border-dashed border-slate-300 text-sm text-slate-500">
              No location or demand evidence is available yet.
            </div>
          )}
          <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3 text-xs text-slate-500"><span>Location evidence</span><span>{locations.length} observed areas</span></div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between"><h2 className="text-lg font-bold text-slate-900">What needs attention</h2><CircleAlert size={19} className="text-amber-500" /></div>
          {records.length ? <div className="mt-4 space-y-3">
            {locations.slice(0, 3).map((item) => <div key={item.location || item.area || item.name} className="flex items-center justify-between rounded-xl bg-slate-50 p-3"><div><p className="text-sm font-bold text-slate-800">{item.location || item.area || item.name}</p><p className="mt-1 text-xs text-slate-500">{item.reason || "Observed operating activity"}</p></div><span className="text-xs font-bold text-blue-700">{item.delay_rate !== undefined ? `${Math.round(item.delay_rate * 100)}% delay` : `${item.record_count ?? item.volume ?? item.deliveries ?? 0} records`}</span></div>)}
          </div> : <div className="mt-4 rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-500">No operational pressure point can be calculated until records arrive.</div>}
          <a href="/ai-analyzer" className="mt-4 inline-flex items-center gap-1 text-sm font-bold text-blue-700 hover:text-blue-900">Open intelligence analyst <ChevronRight size={15} /></a>
        </div>
        {config.id === "distributor" && (
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="mb-3 text-lg font-semibold text-slate-900">
              Distributor operational map
            </h2>
            <OperationsMap
              areaData={overall?.area_hotspots ?? overall?.hotspots ?? []}
              hubLocation={profile?.locations?.[0]}
            />
          </div>
        )}
          <div className="grid gap-6 xl:grid-cols-[1.3fr_.7fr]">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between"><div><h2 className="text-lg font-bold text-slate-900">Operational records</h2><p className="mt-1 text-sm text-slate-500">The latest records backing the metrics above.</p></div><ArrowUpRight size={18} className="text-slate-400" /></div>
              {records.length ? <div className="mt-4 overflow-x-auto"><table className="min-w-full text-left text-sm"><thead className="border-b border-slate-100 text-[10px] font-bold uppercase tracking-wider text-slate-400"><tr><th className="px-2 py-3">Record</th><th className="px-2 py-3">Location</th><th className="px-2 py-3">Status</th><th className="px-2 py-3">Observed value</th></tr></thead><tbody>{records.slice(0, 6).map((record, index) => <tr key={record.id || record.order_id || record.sale_id || record.booking_id || record.shipment_id || index} className="border-b border-slate-50"><td className="px-2 py-3 font-semibold text-slate-700">{record.order_id || record.sale_id || record.booking_id || record.shipment_id || record.product || record.material || "Operational record"}</td><td className="px-2 py-3 text-slate-500">{record.location || record.area || record.region || "—"}</td><td className="px-2 py-3"><span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">{record.status || "Observed"}</span></td><td className="px-2 py-3 font-semibold text-slate-700">{record.amount ?? record.sales ?? record.volume ?? record.units ?? record.demand ?? "—"}</td></tr>)}</tbody></table></div> : <div className="mt-4 rounded-xl border border-dashed border-slate-300 p-5 text-sm text-slate-500">Import or connect records to populate this evidence table.</div>}
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-950 p-5 text-white shadow-sm"><p className="text-xs font-bold uppercase tracking-[0.18em] text-blue-300">Decision readiness</p><h2 className="mt-2 text-2xl font-black">{records.length ? "Evidence available" : "Waiting for evidence"}</h2><p className="mt-3 text-sm leading-6 text-slate-400">{records.length ? "Metrics and attention areas are calculated from the selected operational records. Review evidence before taking action." : "LOGIMIND will not create recommendations, outcomes, or locations without authoritative records."}</p><div className="mt-6 border-t border-white/10 pt-4 text-xs text-slate-500">Confidence is based on record availability and measured fields.</div></div>
          </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { profile, config } = useBusiness();
  const [overall, setOverall] = useState(null);
  const [shipments, setShipments] = useState([]);
  const [agents, setAgents] = useState([]);
  const [agentLocations, setAgentLocations] = useState([]);
  const [locationError, setLocationError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
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
        setError(
          "Dashboard data is unavailable. Check the backend connection and try again.",
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  useEffect(() => {
    if (profile?.businessType && profile.businessType !== "distributor") return undefined;

    let active = true;
    const loadLocations = async () => {
      try {
        const { data } = await getAgentLocations();
        if (active) {
          setAgentLocations(data.locations || []);
          setLocationError("");
        }
      } catch {
        if (active) setLocationError("Live location data is unavailable.");
      }
    };
    loadLocations();
    const interval = window.setInterval(loadLocations, 15000);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, [profile?.businessType]);

  if (profile?.businessType && profile.businessType !== "distributor")
    return <DomainDashboard config={config} profile={profile} />;

  if (loading)
    return <div className="p-6 text-slate-600">Loading dashboard...</div>;
  if (error)
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-800">
        {error}
      </div>
    );

  const metrics = [
    {
      label: "Packages Received",
      value: overall?.total_deliveries ?? 0,
      trend: "Observed",
      icon: Truck,
    },
    {
      label: "Dispatched",
      value: shipments.length,
      trend: "Observed",
      icon: Truck,
    },
    {
      label: "Delivered",
      value: shipments.filter((item) => item.status === "Delivered").length,
      trend: "Observed",
      icon: Clock3,
    },
    {
      label: "Out for Delivery",
      value: shipments.filter((item) => item.status === "Out for Delivery")
        .length,
      trend: "Observed",
      icon: Users,
    },
    {
      label: "Delayed",
      value: shipments.filter((item) => item.status === "Delayed").length,
      trend: "Observed",
      icon: AlertTriangle,
    },
    {
      label: "Failed",
      value: shipments.filter((item) => item.status === "Failed").length,
      trend: "Observed",
      icon: AlertTriangle,
    },
    {
      label: "Avg Delivery Time",
      value: `${overall?.average_delivery_time ?? 0} min`,
      trend: "Observed",
      icon: Clock3,
    },
    {
      label: "Active Delivery Agents",
      value: overall?.active_agents ?? 0,
      trend: "Live",
      icon: Users,
      onClick: () => setShowAgents(true),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map(({ label, value, trend, icon: Icon, onClick }) => (
          <button
            key={label}
            type="button"
            onClick={onClick}
            className="text-left"
            disabled={!onClick}
          >
            <KpiCard label={label} value={value} trend={trend} icon={Icon} />
          </button>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">
              Operational Map
            </h2>
            <span className={`rounded-full px-2 py-1 text-xs font-medium ${
              agentLocations.length ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-600"
            }`}>
              {agentLocations.length ? `${agentLocations.length} live locations` : "No live locations observed"}
            </span>
          </div>
          <OperationsMap
            areaData={overall?.area_hotspots ?? overall?.hotspots ?? []}
            hubLocation={profile?.locations?.[0]}
            agentLocations={agentLocations}
          />
          <p className="mt-2 text-xs text-slate-500">
            {locationError ||
              (agentLocations.length
                ? "Observed agent coordinates refresh every 15 seconds."
                : "Agent coordinates will appear after a device reports them. No coordinates are generated.")}
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-3 text-lg font-semibold text-slate-900">
            Active agents
          </h3>
          <div className="space-y-3">
            {agents.slice(0, 5).map((agent) => (
              <div
                key={agent.agent_id}
                className="rounded-xl border border-slate-200 p-3"
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-800">
                    {agent.agent_id}
                  </span>
                  <Badge tone={agent.status === "Delayed" ? "warning" : "info"}>
                    {agent.status}
                  </Badge>
                </div>
                <p className="mt-2 text-sm text-slate-600">
                  Today&apos;s deliveries: {agent.today_deliveries}
                </p>
                <p className="text-sm text-slate-600">
                  Completed: {agent.completed} · Delayed: {agent.delayed}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <TodayDeliveriesTable shipments={shipments.slice(0, 8)} />
      </div>
      {showAgents && (
        <ActiveAgentsModal
          agents={agents}
          onClose={() => setShowAgents(false)}
        />
      )}
    </div>
  );
}
