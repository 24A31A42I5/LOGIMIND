export default function ExpansionFactors({ candidate, factors }) {
	return <div className="grid grid-cols-2 gap-3 text-sm">{factors.map(({ key, label }) => <div key={key} className="rounded-lg bg-slate-50 p-3"><span className="block text-slate-500">{label}</span><strong className="mt-1 block text-slate-900">{typeof candidate[key] === 'number' ? `${candidate[key]}/100` : candidate[key] || 'Insufficient evidence'}</strong></div>)}</div>;
}
