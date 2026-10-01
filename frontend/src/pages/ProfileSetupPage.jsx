import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { saveProfile } from '../api/profile';
import { BUSINESS_TYPES } from '../config/businessTypes';
import { useBusiness } from '../context/useBusiness';

export default function ProfileSetupPage() {
	const navigate = useNavigate();
	const { setProfile } = useBusiness();
	let user = {};
	try { user = JSON.parse(localStorage.getItem('logimind-user') || '{}'); } catch { localStorage.removeItem('logimind-user'); }
	const [businessType, setBusinessType] = useState('distributor');
	const [businessName, setBusinessName] = useState('My business');
	const [location, setLocation] = useState({ name: 'Main location', latitude: '18.5204', longitude: '73.8567' });
	const [error, setError] = useState('');

	const submit = async (event) => {
		event.preventDefault();
		const profile = { userId: user.userId || 'demo-owner', businessType, businessName, locations: [{ ...location, latitude: Number(location.latitude), longitude: Number(location.longitude) }] };
		try {
			const response = await saveProfile(profile);
			setProfile(response.data);
		} catch (requestError) {
			setProfile(profile);
			setError(requestError.response?.data?.detail || 'Profile service unavailable. Saved for this browser session.');
		}
		localStorage.setItem('logimind-profile', JSON.stringify(profile));
		navigate('/dashboard');
	};

	return <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-10"><form onSubmit={submit} className="w-full max-w-2xl space-y-6 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"><div><p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">Business profile</p><h1 className="mt-2 text-3xl font-bold text-slate-900">Tell LOGIMIND how you operate</h1><p className="mt-2 text-slate-600">Your business type shapes the metrics, evidence, and expansion factors in your workspace.</p></div><div className="grid gap-3 md:grid-cols-2">{BUSINESS_TYPES.map((type) => <button key={type.id} type="button" onClick={() => setBusinessType(type.id)} className={`rounded-xl border p-4 text-left ${businessType === type.id ? 'border-blue-600 bg-blue-50 ring-2 ring-blue-100' : 'border-slate-200'}`}><span className="font-semibold text-slate-900">{type.label}</span><span className="mt-1 block text-sm text-slate-600">{type.description}</span></button>)}</div><div className="grid gap-4 md:grid-cols-2"><label className="text-sm font-medium text-slate-700">Business name<input value={businessName} onChange={(event) => setBusinessName(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5" required /></label><label className="text-sm font-medium text-slate-700">Primary location<input value={location.name} onChange={(event) => setLocation({ ...location, name: event.target.value })} className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5" required /></label><label className="text-sm font-medium text-slate-700">Latitude<input type="number" step="any" value={location.latitude} onChange={(event) => setLocation({ ...location, latitude: event.target.value })} className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5" required /></label><label className="text-sm font-medium text-slate-700">Longitude<input type="number" step="any" value={location.longitude} onChange={(event) => setLocation({ ...location, longitude: event.target.value })} className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5" required /></label></div>{error && <p className="text-sm text-amber-700">{error}</p>}<button className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-500">Open workspace</button></form></div>;
}
