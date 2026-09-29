export default function MapLegend() {
	return (
		<div className="absolute bottom-3 left-3 z-[500] space-y-1 rounded-lg border border-slate-200 bg-white/95 p-3 text-xs text-slate-700 shadow-sm">
			<div><span className="mr-2 inline-block h-2.5 w-2.5 rounded-full bg-blue-600" />Distributor</div>
			<div><span className="mr-2 inline-block h-2.5 w-2.5 rounded-full bg-green-600" />Operational hotspot</div>
			<div><span className="mr-2 inline-block h-2.5 w-2.5 rounded-full bg-red-600" />Problem area</div>
		</div>
	);
}
