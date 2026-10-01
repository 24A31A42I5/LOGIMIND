export default function ColdVsMemoryComparison({
  currentEvidence,
  historicalEvidence,
  memoryAvailable = false,
}) {
  return (
    <section
      className="rounded-xl border border-slate-200 bg-slate-50 p-4"
      aria-labelledby="cold-memory-title"
    >
      <h3
        id="cold-memory-title"
        className="text-lg font-semibold text-slate-900"
      >
        Cold analysis vs remembered analysis
      </h3>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Without memory
          </p>
          <p className="mt-2 text-sm text-slate-700">
            {currentEvidence ||
              "Current operating evidence is not available yet."}
          </p>
        </div>
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">
            With Hindsight
          </p>
          <p className="mt-2 text-sm text-slate-700">
            {memoryAvailable
              ? historicalEvidence
              : "Historical memory currently unavailable."}
          </p>
        </div>
      </div>
    </section>
  );
}
