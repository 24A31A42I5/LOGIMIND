import { useEffect, useState } from 'react';
import { getAgents } from '../api/agents';

export default function DeliveryAgentsPage() {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    getAgents().then((response) => setAgents(response.data)).catch(() => setAgents([]));
  }, []);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">Operations</p>
          <h1 className="text-3xl font-bold text-slate-900">Delivery agents</h1>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {agents.map((agent) => (
          <div key={agent.agent_id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-slate-900">{agent.agent_id}</h2>
              <span className="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-semibold text-blue-700">{agent.status}</span>
            </div>
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              <p>{agent.today_deliveries} deliveries</p>
              <p>{agent.completed} completed</p>
              <p>{agent.delayed} delayed</p>
              <p>{agent.failed} failed</p>
              <p>Average delivery duration: {agent.avg_duration} min</p>
              <p>Total distance: {agent.distance_km} km</p>
              <p>Frequent areas: {agent.frequent_areas.join(', ')}</p>
              <p>Current workload: {agent.current_workload} active deliveries</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
