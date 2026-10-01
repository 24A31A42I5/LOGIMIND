import { useState } from 'react';
import { applyRecommendation, recordRecommendationOutcome } from '../../api/insights';
import Badge from '../common/Badge';

export default function RecommendationCard({ recommendation, memoryAvailable = false, onUpdated }) {
	const [message, setMessage] = useState('');
	const [busy, setBusy] = useState(false);

	const apply = async () => {
		setBusy(true);
		try {
			const id = recommendation.id || 'rec-001';
			await applyRecommendation(id);
			const before = Number(recommendation.before_minutes);
			const after = Number(recommendation.after_minutes);
			if (Number.isFinite(before) && Number.isFinite(after)) {
				await recordRecommendationOutcome(id, before, after);
				setMessage('Applied and measured outcome retained.');
			} else {
				setMessage('Applied. Record an outcome after the intervention is measured.');
			}
			onUpdated?.();
		} catch {
			setMessage('Unable to record this recommendation outcome.');
		} finally {
			setBusy(false);
		}
	};

	return (
		<article className="rounded-xl border border-slate-200 p-4">
			<div className="flex flex-wrap items-start justify-between gap-3">
				<h4 className="text-base font-semibold text-slate-900">{recommendation.title}</h4>
				<Badge tone="info">{recommendation.confidence}% confidence</Badge>
			</div>
			<dl className="mt-3 space-y-2 text-sm text-slate-600">
				<div><dt className="inline font-semibold text-slate-800">Why: </dt><dd className="inline">{recommendation.why}</dd></div>
				<div><dt className="inline font-semibold text-slate-800">Current evidence: </dt><dd className="inline">{recommendation.current_evidence}</dd></div>
				<div><dt className="inline font-semibold text-slate-800">Historical memory: </dt><dd className="inline">{memoryAvailable ? recommendation.historical_memory : 'Historical memory currently unavailable.'}</dd></div>
				<div><dt className="inline font-semibold text-slate-800">Expected impact: </dt><dd className="inline">{recommendation.expected_impact}</dd></div>
			</dl>
			<div className="mt-4 flex items-center gap-3">
				<button type="button" disabled={busy || recommendation.status === 'Applied'} onClick={apply} className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300">{recommendation.status === 'Applied' ? 'Applied' : 'Apply recommendation'}</button>
				{message && <span className="text-sm text-slate-600">{message}</span>}
			</div>
		</article>
	);
}
