import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/client';
import { useBusiness } from '../context/useBusiness';

const content = {
  '/orders': ['Orders', 'Track ordering patterns, peak periods, and delivery demand.', ['Orders today', 'Repeat customers', 'Peak period']],
  '/sales': ['Sales', 'Understand revenue movement and the products or services creating demand.', ['Sales today', 'Growth trend', 'Top category']],
  '/analytics': ['Analytics', 'Compare current operating signals with the evidence behind expansion decisions.', ['Demand trend', 'Customer density', 'Coverage']],
  '/hotspots': ['Hotspots', 'See where customer demand is concentrating before choosing an action.', ['Strongest area', 'Demand signal', 'Coverage gap']],
  '/supplies': ['Supplies', 'Monitor material movement and B2B supply coverage.', ['Supply volume', 'Open orders', 'Delivery areas']],
  '/customers': ['Customers', 'Understand customer concentration and service opportunities.', ['Active customers', 'Repeat rate', 'Top area']],
  '/demand': ['Demand', 'Translate business-specific demand into reusable intelligence signals.', ['Current demand', 'Growth trend', 'Demand areas']],
  '/products': ['Products', 'Track product movement and the demand patterns behind it.', ['Products tracked', 'Fast movers', 'Stock signal']],
  '/bookings': ['Bookings', 'Understand appointment demand and service capacity.', ['Bookings today', 'Peak period', 'Open requests']],
  '/service-areas': ['Service Areas', 'Compare service radius, booking demand, and operational reach.', ['Active areas', 'Coverage gap', 'Travel load']],
};

export default function DomainWorkspacePage() {
  const { pathname } = useLocation();
  const { config } = useBusiness();
  const [title, description, metrics] = content[pathname] || content['/analytics'];
  const [records, setRecords] = useState([]);
  const [state, setState] = useState('loading');

  useEffect(() => {
    api.get(config.operationalEndpoint).then(({ data }) => {
      setRecords(data.records || []);
      setState(data.synthetic ? 'synthetic' : 'ready');
    }).catch(() => setState('error'));
  }, [config.operationalEndpoint]);

  const metricValues = [records.length, records.reduce((sum, record) => sum + Number(record.demand || record.sales || record.volume || record.units || 0), 0), new Set(records.map((record) => record.location)).size];
  return <div className="space-y-6"><div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">{config.label}</p><h1 className="mt-1 text-3xl font-bold text-slate-900">{title}</h1><p className="mt-2 text-slate-600">{description}</p></div>{state === 'synthetic' && <p className="rounded-lg bg-slate-200 px-3 py-2 text-sm text-slate-700">Synthetic demo data. These signals are representative and are not external geographic evidence.</p>}{state === 'error' && <p className="rounded-lg bg-amber-50 p-4 text-amber-800">{title} data is unavailable. Check the domain service and try again.</p>}{state !== 'loading' && state !== 'error' && <div className="grid gap-4 md:grid-cols-3">{metrics.slice(0, 3).map((metric, index) => <div key={metric} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm text-slate-500">{metric}</p><p className="mt-3 text-3xl font-bold text-slate-900">{metricValues[index] ?? 0}</p><p className="mt-2 text-sm text-slate-600">Current operating signal</p></div>)}</div>}{state === 'loading' && <p className="text-slate-600">Loading {title.toLowerCase()}...</p>}</div>;
}