export default function TodayDeliveriesTable({ shipments = [] }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left text-sm text-slate-700">
        <thead className="bg-slate-50 text-xs uppercase tracking-[0.12em] text-slate-600">
          <tr>
            <th className="px-3 py-3">Shipment</th>
            <th className="px-3 py-3">Customer</th>
            <th className="px-3 py-3">Area</th>
            <th className="px-3 py-3">Agent</th>
            <th className="px-3 py-3">Status</th>
            <th className="px-3 py-3">Dispatch</th>
            <th className="px-3 py-3">Expected</th>
            <th className="px-3 py-3">Duration</th>
          </tr>
        </thead>
        <tbody>
          {shipments.map((shipment) => (
            <tr key={shipment.shipment_id} className="border-t border-slate-200">
              <td className="px-3 py-3 font-medium text-slate-800">{shipment.shipment_id}</td>
              <td className="px-3 py-3">{shipment.customer}</td>
              <td className="px-3 py-3">{shipment.area}</td>
              <td className="px-3 py-3">{shipment.agent_id}</td>
              <td className="px-3 py-3">
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">
                  {shipment.status}
                </span>
              </td>
              <td className="px-3 py-3">{new Date(shipment.dispatch_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
              <td className="px-3 py-3">{new Date(shipment.expected_delivery).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
              <td className="px-3 py-3">{shipment.duration_minutes} min</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
