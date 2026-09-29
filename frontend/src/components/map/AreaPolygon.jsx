import { Polygon, Popup } from 'react-leaflet';

const toCoordinate = (value, minimum, maximum) => {
	if (value === undefined || value === null || (typeof value === 'string' && value.trim() === '')) return null;
	const number = typeof value === 'number' ? value : Number(value);
	return Number.isFinite(number) && number >= minimum && number <= maximum ? number : null;
};

export default function AreaPolygon({ name, coords, performance = 'Healthy', info }) {
	const validCoords = Array.isArray(coords) && coords
		.map((point) => {
			if (!Array.isArray(point) || point.length < 2) return null;
			const latitude = toCoordinate(point[0], -90, 90);
			const longitude = toCoordinate(point[1], -180, 180);
			return latitude === null || longitude === null ? null : [latitude, longitude];
		})
		.filter(Boolean);

	if (validCoords.length < 3) {
		if (import.meta.env.DEV) console.warn('[LOGIMIND] Skipping invalid map polygon:', { name, coords });
		return null;
	}

	const isProblem = performance === 'Problem' || performance === 'Critical';
	const color = isProblem ? '#dc2626' : '#16a34a';
	return (
		<Polygon positions={validCoords} pathOptions={{ color, fillColor: color, fillOpacity: 0.28, weight: 2 }}>
			<Popup><strong>{name}</strong><br />{info || `${performance} operational area`}</Popup>
		</Polygon>
	);
}
