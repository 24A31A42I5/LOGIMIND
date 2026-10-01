export default function ExpansionRecommendation({ candidate }) {
	return <div className="border-t border-slate-100 pt-4"><p className="text-sm font-semibold text-slate-800">Why this location</p><p className="mt-1 text-sm text-slate-600">{candidate.reason || 'Evidence is not sufficient to explain this candidate.'}</p><p className="mt-4 text-sm font-semibold text-slate-800">Historical memory</p><p className="mt-1 text-sm text-slate-600">{candidate.historical_evidence || 'Historical memory is unavailable.'}</p></div>;
}
