import { X } from 'lucide-react';
import Badge from '../common/Badge';

export default function ActiveAgentsModal({ agents, onClose }) {
	return (
		<div className="fixed inset-0 z-[1100] flex items-center justify-center bg-slate-950/40 p-4" role="dialog" aria-modal="true" aria-labelledby="active-agents-title">
			<div className="max-h-[85vh] w-full max-w-2xl overflow-y-auto rounded-xl bg-white p-5 shadow-xl">
				<div className="flex items-center justify-between border-b border-slate-200 pb-3">
					<h2 id="active-agents-title" className="text-lg font-semibold text-slate-900">Active delivery agents</h2>
					<button type="button" onClick={onClose} aria-label="Close active agents" className="rounded-md p-2 text-slate-500 hover:bg-slate-100"><X size={18} /></button>
				</div>
				<div className="mt-4 grid gap-3 sm:grid-cols-2">
					{agents.map((agent) => (
						<div key={agent.agent_id} className="rounded-lg border border-slate-200 p-3">
							<div className="flex items-center justify-between"><strong>{agent.agent_id}</strong><Badge tone={agent.status === 'Delayed' ? 'warning' : 'info'}>{agent.status}</Badge></div>
							<div className="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-600"><span>Deliveries: {agent.today_deliveries}</span><span>Completed: {agent.completed}</span><span>Delayed: {agent.delayed}</span><span>Failed: {agent.failed}</span><span className="col-span-2">Active workload: {agent.current_workload}</span></div>
						</div>
					))}
				</div>
			</div>
		</div>
	);
}
