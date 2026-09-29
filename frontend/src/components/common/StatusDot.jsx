const colors = {
	Delivered: 'bg-green-500',
	Healthy: 'bg-green-500',
	Assigned: 'bg-blue-500',
	'Out for Delivery': 'bg-blue-500',
	Delayed: 'bg-amber-500',
	Failed: 'bg-red-500',
	Problem: 'bg-red-500',
};

export default function StatusDot({ status = 'Unknown' }) {
	return <span className="inline-flex items-center gap-2"><span className={`h-2 w-2 rounded-full ${colors[status] || 'bg-slate-400'}`} aria-hidden="true" /><span>{status}</span></span>;
}
