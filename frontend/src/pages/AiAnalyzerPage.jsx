import { useEffect, useState } from 'react';
import { BarChart, Bar, ResponsiveContainer, XAxis, YAxis, Tooltip, LineChart, Line, CartesianGrid, AreaChart, Area } from 'recharts';
import { getOverallAnalytics, getDailyAnalytics, getAreaAnalytics } from '../api/analytics';
import { getTodayInsights, investigateArea } from '../api/insights';
import { getRecentMemory } from '../api/memory';
import RecommendationCard from '../components/ai/RecommendationCard';
import MemoryEvidenceModal from '../components/ai/MemoryEvidenceModal';
import ColdVsMemoryComparison from '../components/ai/ColdVsMemoryComparison';

const hourData = [
  { time: '08', deliveries: 26 },
  { time: '10', deliveries: 40 },
  { time: '12', deliveries: 64 },
  { time: '14', deliveries: 72 },
  { time: '16', deliveries: 91 },
  { time: '18', deliveries: 120 },
  { time: '20', deliveries: 94 },
];

const areaData = [
  { area: 'Area A', avg: 39 },
  { area: 'Area B', avg: 42 },
  { area: 'Area C', avg: 47 },
  { area: 'Area D', avg: 53 },
];

export default function AiAnalyzerPage() {
  const [overall, setOverall] = useState(null);
  const [daily, setDaily] = useState(null);
  const [areas, setAreas] = useState([]);
  const [insights, setInsights] = useState(null);
  const [investigation, setInvestigation] = useState(null);
  const [memories, setMemories] = useState([]);
  const [showMemory, setShowMemory] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [overallRes, dailyRes, areaRes, insightRes, memoryRes] = await Promise.all([
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
        const investigationRes = await investigateArea('Area C');
        setInvestigation(investigationRes.data);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (loading) return <div className="p-6 text-slate-600">Loading analytics...</div>;

  const trendData = [
    { date: 'Aug 05', value: 42 },
    { date: 'Aug 10', value: 45 },
    { date: 'Aug 15', value: 47 },
    { date: 'Aug 20', value: 44 },
    { date: 'Aug 28', value: 41 },
  ];
  const volumeByHour = daily?.timeline?.map((item) => ({ time: item.time, deliveries: item.deliveries })) || hourData;
  const averageByArea = areas.length ? areas.map((item) => ({ area: item.area, avg: item.average_delivery_time })) : areaData;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">AI analyzer</p>
        <h1 className="text-3xl font-bold text-slate-900">Overall analytics</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Total deliveries</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{overall?.total_deliveries ?? 0}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Average delivery time</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{overall?.average_delivery_time ?? 0} min</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Delay rate</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{overall?.delay_rate ?? 0}%</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Failed delivery rate</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{overall?.failed_delivery_rate ?? 0}%</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Active agents</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{overall?.active_agents ?? 0}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Major hotspots</p>
          <p className="mt-2 text-xl font-bold text-slate-900">{overall?.area_hotspots?.[0]?.name ?? 'Area C'}</p>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">Delivery volume by hour</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={volumeByHour}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="deliveries" fill="#2563eb" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">Average delivery time by area</h3>
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
          <h3 className="mb-4 text-lg font-semibold text-slate-900">Delivery volume over time</h3>
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
          <h3 className="mb-4 text-lg font-semibold text-slate-900">Average delivery time trend</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} />
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
            {insights?.insights?.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-900">AI recommendations</h3>
        <div className="mt-4 space-y-4">
          {investigation?.recommendations?.map((recommendation) => (
            <RecommendationCard key={recommendation.title} recommendation={recommendation} memoryAvailable={investigation.memory_available} />
          ))}
        </div>
        <button type="button" onClick={() => setShowMemory(true)} className="mt-4 rounded-lg border border-blue-200 px-3 py-2 text-sm font-semibold text-blue-700 hover:bg-blue-50">View memory evidence</button>
      </div>

      <ColdVsMemoryComparison
        currentEvidence={investigation?.summary}
        historicalEvidence="Area C has repeatedly experienced evening delays, and a previous two-agent intervention reduced delivery time from 48 to 31 minutes."
        memoryAvailable={investigation?.memory_available}
      />
      {showMemory && <MemoryEvidenceModal memories={investigation?.memory_available ? memories : []} onClose={() => setShowMemory(false)} />}
    </div>
  );
}
