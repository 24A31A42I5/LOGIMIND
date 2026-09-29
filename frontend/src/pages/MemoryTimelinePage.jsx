import { useEffect, useState } from 'react';
import { getRecentMemory, getMemoryStats } from '../api/memory';

export default function MemoryTimelinePage() {
  const [memories, setMemories] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    Promise.all([getRecentMemory(), getMemoryStats()]).then(([memoriesRes, statsRes]) => {
      setMemories(memoriesRes.data);
      setStats(statsRes.data);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">Hindsight</p>
        <h1 className="text-3xl font-bold text-slate-900">Operational memory</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Memories</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{stats?.total_memories ?? 0}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Successful interventions</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{stats?.successful_interventions ?? 0}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Unsuccessful interventions</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{stats?.unsuccessful_interventions ?? 0}</p>
        </div>
      </div>

      <div className="space-y-4">
        {memories.map((memory, index) => (
          <div key={memory.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-3">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
                {index + 1}
              </span>
              <div>
                <p className="text-sm font-medium text-slate-500">{memory.date}</p>
                <h3 className="text-xl font-semibold text-slate-900">{memory.title}</h3>
              </div>
            </div>
            <p className="mt-4 text-slate-600">{memory.summary}</p>
            <ul className="mt-3 list-disc space-y-1 pl-5 text-slate-600">
              {memory.evidence.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
