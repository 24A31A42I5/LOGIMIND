import { useEffect, useState } from 'react';
import { getShipments } from '../api/shipments';

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    getShipments().then((response) => setShipments(response.data)).catch(() => setError('Shipment data is unavailable.'));
  }, []);

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">Operations</p>
        <h1 className="text-3xl font-bold text-slate-900">Shipments</h1>
      </div>

      {error && <p className="rounded-lg bg-amber-50 p-4 text-amber-800">{error}</p>}
      {!error && !shipments.length && <p className="rounded-lg bg-slate-50 p-4 text-slate-600">No shipments are available for this workspace.</p>}
      <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full text-left text-sm text-slate-700">
          <thead className="bg-slate-50 text-xs uppercase tracking-[0.12em] text-slate-600">
            <tr>
              <th className="px-4 py-3">Shipment</th>
              <th className="px-4 py-3">Product</th>
              <th className="px-4 py-3">Customer</th>
              <th className="px-4 py-3">Area</th>
              <th className="px-4 py-3">Agent</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Dispatch</th>
              <th className="px-4 py-3">Expected</th>
            </tr>
          </thead>
          <tbody>
            {shipments.slice(0, 12).map((shipment) => (
              <tr key={shipment.shipment_id} className="border-t border-slate-200">
                <td className="px-4 py-3 font-medium text-slate-800">{shipment.shipment_id}</td>
                <td className="px-4 py-3">{shipment.product}</td>
                <td className="px-4 py-3">{shipment.customer}</td>
                <td className="px-4 py-3">{shipment.area}</td>
                <td className="px-4 py-3">{shipment.agent_id}</td>
                <td className="px-4 py-3">
                  <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700">
                    {shipment.status}
                  </span>
                </td>
                <td className="px-4 py-3">{new Date(shipment.dispatch_time).toLocaleString()}</td>
                <td className="px-4 py-3">{new Date(shipment.expected_delivery).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
