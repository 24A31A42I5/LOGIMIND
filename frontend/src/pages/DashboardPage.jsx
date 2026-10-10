import { useEffect, useState } from "react";
import api from "../api/client";
import { getOverallAnalytics } from "../api/analytics";
import { getShipments } from "../api/shipments";
import { getAgentLocations, getAgents } from "../api/agents";
import OperationsMap from "../components/map/OperationsMap";
import KpiCard from "../components/dashboard/KpiCard";
import TodayDeliveriesTable from "../components/dashboard/TodayDeliveriesTable";
import { Users, Truck, Clock3, AlertTriangle } from "lucide-react";
import ActiveAgentsModal from "../components/dashboard/ActiveAgentsModal";
import Badge from "../components/common/Badge";
import { useBusiness } from "../context/useBusiness";

function DomainDashboard({ config, profile }) {
  const [records, setRecords] = useState([]);
  const [state, setState] = useState("loading");
  const [overall, setOverall] = useState(null);

  useEffect(() => {
    api
      .get(config.operationalEndpoint)
      .then(({ data }) => {
        setRecords(data.records || []);
        setState("ready");
      })
      .catch(() => setState("error"));
  }, [config.operationalEndpoint]);

  useEffect(() => {
    getOverallAnalytics()
      .then(({ data }) => setOverall(data))
      .catch(() => setOverall(null));
  }, []);

  if (state === "loading")
    return (
      <div className="p-6 text-slate-600">
        Loading {config.label.toLowerCase()} operations...
      </div>
    );
  if (state === "error")
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-800">
        {config.label} operational data is unavailable.
      </div>
    );
  const values =
    config.id === "restaurant"
      ? [
          records.length,
          records.reduce(
            (sum, record) => sum + Number(record.sales || record.amount || 0),
            0,
          ),
          records.reduce((sum, record) => sum + Number(record.demand || 0), 0),
          new Set(records.map((record) => record.location)).size,
        ]
      : config.id === "raw_material"
        ? [
            records.reduce(
              (sum, record) =>
                sum + Number(record.volume || record.quantity || 0),
              0,
            ),
            records.reduce(
              (sum, record) => sum + Number(record.demand || 0),
              0,
            ),
            new Set(records.map((record) => record.customer)).size,
            new Set(records.map((record) => record.location)).size,
          ]
        : [
            records.reduce(
              (sum, record) => sum + Number(record.units || record.sales || 0),
              0,
            ),
            new Set(records.map((record) => record.product)).size,
            new Set(records.map((record) => record.customer)).size,
            records.reduce(
              (sum, record) => sum + Number(record.demand || 0),
              0,
            ),
          ];
  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">
          {config.label} workspace
        </p>
        <h1 className="mt-1 text-3xl font-bold text-slate-900">
          Current operations
        </h1>
        <p className="mt-2 text-slate-600">
          Business-specific signals for demand, performance, and expansion
          readiness.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {config.metrics.map((metric, index) => (
          <div
            key={metric}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <p className="text-sm text-slate-500">{metric}</p>
            <p className="mt-3 text-3xl font-bold text-slate-900">
              {values[index] ?? 0}
            </p>
            <p className="mt-2 text-sm text-slate-600">
              Current operating signal
            </p>
          </div>
        ))}
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="mb-3 text-lg font-semibold text-slate-900">
            {config.label} operational map
          </h2>
          <OperationsMap
            areaData={overall?.hotspots ?? []}
            hubLocation={profile?.locations?.[0]}
          />
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">
            Observed performance
          </h2>
          <p className="mt-3 text-sm text-slate-600">
            Trend:{" "}
            <span className="font-semibold text-slate-900">
              {overall?.trend ??
                overall?.currentData?.trend ??
                "insufficient evidence"}
            </span>
          </p>
          <p className="mt-2 text-sm text-slate-600">
            Top location:{" "}
            <span className="font-semibold text-slate-900">
              {overall?.hotspots?.[0]?.location ?? "No location yet"}
            </span>
          </p>
          <p className="mt-2 text-sm text-slate-600">
            Observed locations:{" "}
            <span className="font-semibold text-slate-900">
              {overall?.hotspots?.length ?? 0}
            </span>
          </p>
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
