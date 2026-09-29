import { useState } from 'react';
import {
	closeDay,
	loadDay,
	resetDemo,
	triggerAreaCDelay,
	triggerFailedDeliveryHotspot,
	triggerSuccessfulIntervention,
} from '../../api/demo';

export default function DemoToolbar() {
	const [message, setMessage] = useState('');
	const [busy, setBusy] = useState(false);

	const run = async (action) => {
		setBusy(true);
		try {
			const response = await action();
			setMessage(response.data.message || 'Demo action completed.');
		} catch {
			setMessage('Demo action could not be completed.');
		} finally {
			setBusy(false);
		}
	};

	return (
		<aside className="fixed bottom-4 left-4 right-4 z-[1000] mx-auto max-w-5xl rounded-xl border border-slate-300 bg-white/95 p-3 shadow-lg backdrop-blur lg:left-auto lg:right-6 lg:max-w-3xl">
			<div className="flex flex-wrap items-center gap-2">
				<span className="mr-1 text-xs font-semibold uppercase tracking-wide text-slate-500">Demo controls</span>
				<button type="button" disabled={busy} onClick={() => run(resetDemo)} className="rounded-md border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50">Reset</button>
				{[1, 7, 15, 30].map((day) => (
					<button key={day} type="button" disabled={busy} onClick={() => run(() => loadDay(day))} className="rounded-md border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50">Day {day}</button>
				))}
				<button type="button" disabled={busy} onClick={() => run(triggerAreaCDelay)} className="rounded-md bg-amber-100 px-2 py-1 text-xs font-medium text-amber-800 hover:bg-amber-200">Trigger delay</button>
				<button type="button" disabled={busy} onClick={() => run(triggerFailedDeliveryHotspot)} className="rounded-md bg-red-100 px-2 py-1 text-xs font-medium text-red-800 hover:bg-red-200">Trigger failure</button>
				<button type="button" disabled={busy} onClick={() => run(triggerSuccessfulIntervention)} className="rounded-md bg-green-100 px-2 py-1 text-xs font-medium text-green-800 hover:bg-green-200">Record success</button>
				<button type="button" disabled={busy} onClick={() => run(closeDay)} className="rounded-md bg-blue-600 px-2 py-1 text-xs font-semibold text-white hover:bg-blue-700">Close day</button>
			</div>
			{message && <p className="mt-2 text-xs text-slate-600">{message}</p>}
		</aside>
	);
}
