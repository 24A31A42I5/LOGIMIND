import ExpansionFactors from './ExpansionFactors';
import ExpansionRecommendation from './ExpansionRecommendation';

export default function LocationScoreCard({ candidate, factors }) {
	return <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-start justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Expansion opportunity</p><h2 className="mt-1 text-2xl font-bold text-slate-900">{candidate.name}</h2></div><span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-700">{candidate.category}</span></div><div className="mt-5"><ExpansionFactors candidate={candidate} factors={factors} /></div><div className="mt-5"><ExpansionRecommendation candidate={candidate} /></div></article>;
}
