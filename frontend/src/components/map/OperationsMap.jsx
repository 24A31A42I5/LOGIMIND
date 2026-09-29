import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import AreaPolygon from './AreaPolygon';
import MapLegend from './MapLegend';

const blueIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const fallbackPolygons = [
  { name: 'Area C', performance: 'Hotspot', coords: [[18.502, 73.84], [18.52, 73.856], [18.508, 73.863], [18.5, 73.848]], info: 'Deliveries: 284 • Average duration: 49 min • Delay rate: 21% • Peak: 6 PM – 8 PM' },
  { name: 'Area D', performance: 'Problem', coords: [[18.542, 73.875], [18.558, 73.892], [18.546, 73.897], [18.538, 73.882]], info: 'Deliveries: 198 • Average duration: 53 min • Delay rate: 25% • Peak: 4 PM – 6 PM' },
];

const toCoordinate = (value, minimum, maximum) => {
  if (value === undefined || value === null || (typeof value === 'string' && value.trim() === '')) return null;
  const number = typeof value === 'number' ? value : Number(value);
  return Number.isFinite(number) && number >= minimum && number <= maximum ? number : null;
};

const getAreaCoordinate = (area, primaryName, alternateName, minimum, maximum) => (
  toCoordinate(area[primaryName] ?? area[alternateName], minimum, maximum)
);

export default function OperationsMap({ areaData = [] }) {
  const center = [18.52, 73.8567];
  const distributorLatitude = toCoordinate(18.5204, -90, 90);
  const distributorLongitude = toCoordinate(73.8567, -180, 180);
  const polygons = areaData.length ? areaData.flatMap((area) => {
    const latitude = getAreaCoordinate(area, 'lat', 'latitude', -90, 90);
    const longitude = getAreaCoordinate(area, 'lng', 'longitude', -180, 180);
    if (latitude === null || longitude === null) {
      if (import.meta.env.DEV) console.warn('[LOGIMIND] Skipping area without valid map coordinates:', area);
      return [];
    }
    return [{
      name: area.name,
      performance: area.performance || (area.name === 'Area C' ? 'Hotspot' : 'Healthy'),
      coords: [[latitude - 0.009, longitude - 0.008], [latitude + 0.009, longitude], [latitude, longitude + 0.009], [latitude - 0.009, longitude + 0.004]],
      info: `Deliveries: ${area.deliveries ?? 'n/a'} • Average duration: ${area.average_delivery_time ?? 'n/a'} min`,
    }];
  }) : fallbackPolygons;

  return (
    <div className="relative h-[420px] w-full overflow-hidden rounded-xl border border-slate-200">
      <MapContainer center={center} zoom={12} scrollWheelZoom className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {distributorLatitude !== null && distributorLongitude !== null && (
          <Marker position={[distributorLatitude, distributorLongitude]} icon={blueIcon}>
            <Popup>Distributor Location</Popup>
          </Marker>
        )}

        {polygons.map((polygon) => <AreaPolygon key={polygon.name} {...polygon} />)}
      </MapContainer>
      <MapLegend />
    </div>
  );
}
