const tones = {
	neutral: 'bg-slate-100 text-slate-700',
	success: 'bg-green-100 text-green-800',
	warning: 'bg-amber-100 text-amber-800',
	critical: 'bg-red-100 text-red-800',
	info: 'bg-blue-100 text-blue-800',
};

export default function Badge({ children, tone = 'neutral' }) {
	return <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-semibold ${tones[tone]}`}>{children}</span>;
}
