import { useState } from 'react';
import { applyRecommendation, executeRecommendation } from '../../api/insights';
import Badge from '../common/Badge';

export default function RecommendationCard({ recommendation, memoryAvailable = false, onUpdated }) {
	const [message, setMessage] = useState('');
	const [busy, setBusy] = useState(false);
	const [status, setStatus] = useState(recommendation.status);
	const [shipmentId, setShipmentId] = useState('');
	const [agentId, setAgentId] = useState('');

	const apply = async () => {
		setBusy(true);
		try {
			if (!recommendation.id) {
				setMessage('This recommendation has no persisted approval ID and cannot be applied.');
				return;
			}
			const id = recommendation.id;
			await applyRecommendation(id);
			setStatus('Approved');
			setMessage('Approved and recorded. Execution and outcome remain pending until the supported operational action is completed.');
			onUpdated?.();
		} catch {
			setMessage('Unable to record this recommendation outcome.');
		} finally {
			setBusy(false);
		}
	};

	const execute = async () => {
		setBusy(true);
		try {
			if (!recommendation.id || !shipmentId || !agentId) {
				setMessage('Enter an existing shipment ID and delivery agent ID to execute this action.');
				return;
			}
			await executeRecommendation(recommendation.id, shipmentId, agentId);
			setStatus('Executed');
			setMessage('Dispatch reassignment executed against the operational shipment record. Measure a new observation before recording an outcome.');
			onUpdated?.();
		} catch {
			setMessage('The action could not be executed. Verify the shipment and agent belong to this business.');
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
				{status !== 'Approved' && status !== 'Executed' && <button type="button" disabled={busy || !recommendation.id} onClick={apply} className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300">Approve action</button>}
				{status === 'Approved' && (
					<div className="flex flex-wrap items-center gap-2">
						<input value={shipmentId} onChange={(event) => setShipmentId(event.target.value)} placeholder="Shipment ID" className="w-32 rounded-lg border border-slate-300 px-3 py-2 text-sm" />
						<input value={agentId} onChange={(event) => setAgentId(event.target.value)} placeholder="Agent ID" className="w-28 rounded-lg border border-slate-300 px-3 py-2 text-sm" />
						<button type="button" disabled={busy} onClick={execute} className="rounded-lg bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300">Execute dispatch</button>
					</div>
				)}
				{status === 'Executed' && <Badge tone="success">Executed</Badge>}
				{message && <span className="text-sm text-slate-600">{message}</span>}
			</div>
		</article>
	);
}
