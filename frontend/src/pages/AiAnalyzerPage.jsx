import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  LineChart,
  Line,
  CartesianGrid,
  AreaChart,
  Area,
} from "recharts";
import {
  getOverallAnalytics,
  getDailyAnalytics,
  getAreaAnalytics,
} from "../api/analytics";
import { getTodayInsights, investigateArea } from "../api/insights";
import { getRecentMemory } from "../api/memory";
import RecommendationCard from "../components/ai/RecommendationCard";
import MemoryEvidenceModal from "../components/ai/MemoryEvidenceModal";
import ColdVsMemoryComparison from "../components/ai/ColdVsMemoryComparison";
import { useBusiness } from "../context/useBusiness";

export default function AiAnalyzerPage() {
  const { profile } = useBusiness();
  const [overall, setOverall] = useState(null);
  const [daily, setDaily] = useState(null);
  const [areas, setAreas] = useState([]);
  const [insights, setInsights] = useState(null);
  const [investigation, setInvestigation] = useState(null);
  const [memories, setMemories] = useState([]);
  const [showMemory, setShowMemory] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [overallRes, dailyRes, areaRes, insightRes, memoryRes] =
          await Promise.all([
            getOverallAnalytics(),
            getDailyAnalytics(),
            getAreaAnalytics(),
            getTodayInsights(),
            getRecentMemory(),
          ]);
        setOverall(overallRes.data);
        setDaily(dailyRes.data);
        setAreas(areaRes.data);
        setInsights(insightRes.data);
        setMemories(memoryRes.data);
        const investigationRes = await investigateArea();
        setInvestigation(investigationRes.data);
      } catch {
        setError("AI analysis is unavailable right now.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [profile?.businessType]);

  if (loading)
    return <div className="p-6 text-slate-600">Loading analytics...</div>;
  if (error)
    return (
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-6 text-amber-800">
        {error}
      </div>
    );

  const metrics = overall?.currentData || overall || {};
  const locationKey =
    profile?.businessType === "distributor" ? "area" : "location";
  const volumeKey =
    profile?.businessType === "distributor" ? "deliveries" : "volume";
  const volumeByHour =
    daily?.timeline ||
    areas.map((item) => ({
      time: item[locationKey],
      [volumeKey]: item.volume || item.deliveries || item.demand || 0,
    }));
  const averageByArea = areas.map((item) => ({
    area: item[locationKey] || item.area,
    avg: item.average_delivery_time || item.demand || item.performance || 0,
  }));
  const trendData =
    daily?.timeline?.map((item) => ({
      date: item.time,
      value: item.deliveries || item.volume || item.demand || 0,
    })) ||
    areas.map((item) => ({
      date: item[locationKey] || item.area,
      value: item.volume || item.demand || item.deliveries || 0,
    }));

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
          AI analyzer
        </p>
        <h1 className="text-3xl font-bold text-slate-900">
          {profile?.businessName || "Business"} intelligence
        </h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Current volume</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">
            {metrics.volume ?? 0}
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Demand</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">
            {metrics.demand ?? 0}
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Growth</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">
            {metrics.growth ?? 0}
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Performance</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">
            {metrics.performance ?? 0}
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Coverage</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">
            {metrics.coverage ?? 0}
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Top location</p>
          <p className="mt-2 text-xl font-bold text-slate-900">
            {metrics.hotspots?.[0]?.location ||
              metrics.area_hotspots?.[0]?.name ||
              "No location yet"}
          </p>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Demand by operating context
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={volumeByHour}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Bar dataKey={volumeKey} fill="#2563eb" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Location performance
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={averageByArea}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="area" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="avg" fill="#16a34a" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Volume over time
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="fillArea" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.05} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area dataKey="value" stroke="#2563eb" fill="url(#fillArea)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Performance trend
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#f59e0b"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-900">AI insight</h3>
        <div className="mt-3 rounded-xl bg-slate-50 p-4">
          <p className="font-medium text-slate-800">{insights?.summary}</p>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-600">
            {insights?.insights?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-900">
          AI recommendations
        </h3>
        <div className="mt-4 space-y-4">
          {investigation?.recommendations?.map((recommendation) => (
            <RecommendationCard
              key={recommendation.title}
              recommendation={recommendation}
              memoryAvailable={investigation.memory_available}
            />
          ))}
        </div>
        <button
          type="button"
          onClick={() => setShowMemory(true)}
          className="mt-4 rounded-lg border border-blue-200 px-3 py-2 text-sm font-semibold text-blue-700 hover:bg-blue-50"
        >
          View memory evidence
        </button>
      </div>

      <ColdVsMemoryComparison
        currentEvidence={investigation?.summary}
        historicalEvidence={
          investigation?.historicalEvidence?.message ||
          "No historical evidence is currently available."
        }
        memoryAvailable={investigation?.memory_available}
      />
      {showMemory && (
        <MemoryEvidenceModal
          memories={investigation?.memory_available ? memories : []}
          onClose={() => setShowMemory(false)}
        />
      )}
    </div>
  );
}
