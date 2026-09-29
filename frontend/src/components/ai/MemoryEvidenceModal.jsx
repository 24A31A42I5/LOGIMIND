import { X } from 'lucide-react';

export default function MemoryEvidenceModal({ memories = [], onClose }) {
	return (
		<div className="fixed inset-0 z-[1100] flex items-center justify-center bg-slate-950/40 p-4" role="dialog" aria-modal="true" aria-labelledby="memory-evidence-title">
			<div className="max-h-[85vh] w-full max-w-xl overflow-y-auto rounded-xl bg-white p-5 shadow-xl">
				<div className="flex items-center justify-between border-b border-slate-200 pb-3">
					<h2 id="memory-evidence-title" className="text-lg font-semibold text-slate-900">Historical memory evidence</h2>
					<button type="button" onClick={onClose} aria-label="Close memory evidence" className="rounded-md p-2 text-slate-500 hover:bg-slate-100"><X size={18} /></button>
				</div>
				{memories.length ? <div className="mt-4 space-y-3">{memories.map((memory) => <div key={memory.id || memory.title} className="rounded-lg border border-slate-200 p-3"><p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{memory.date}</p><h3 className="mt-1 font-semibold text-slate-900">{memory.title}</h3><p className="mt-1 text-sm text-slate-600">{memory.summary}</p></div>)}</div> : <p className="mt-4 text-sm text-slate-600">Historical memory currently unavailable.</p>}
			</div>
		</div>
	);
}
