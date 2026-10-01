import LocationScoreCard from './LocationScoreCard';

export default function CandidateLocations({ candidates, factors }) {
	if (!candidates.length) return <p className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-amber-800">Insufficient evidence for a reliable expansion assessment.</p>;
	return <div className="grid gap-5 lg:grid-cols-2">{candidates.map((candidate) => <LocationScoreCard key={candidate.name} candidate={candidate} factors={factors} />)}</div>;
}
