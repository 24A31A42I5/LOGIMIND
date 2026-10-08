import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import AreaPolygon from "./AreaPolygon";
import MapLegend from "./MapLegend";

const blueIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const toCoordinate = (value, minimum, maximum) => {
  if (
    value === undefined ||
    value === null ||
    (typeof value === "string" && value.trim() === "")
  )
    return null;
  const number = typeof value === "number" ? value : Number(value);
  return Number.isFinite(number) && number >= minimum && number <= maximum
    ? number
    : null;
};

const getAreaCoordinate = (
  area,
  primaryName,
  alternateName,
  minimum,
  maximum,
) => toCoordinate(area[primaryName] ?? area[alternateName], minimum, maximum);

export default function OperationsMap({ areaData = [], hubLocation = null }) {
  const hubLatitude = toCoordinate(hubLocation?.latitude, -90, 90);
  const hubLongitude = toCoordinate(hubLocation?.longitude, -180, 180);
  const firstPoint = areaData.find(
    (area) => getAreaCoordinate(area, "lat", "latitude", -90, 90) !== null,
  );
  const center = [
    hubLatitude ??
      getAreaCoordinate(firstPoint || {}, "lat", "latitude", -90, 90) ??
      0,
    hubLongitude ??
      getAreaCoordinate(firstPoint || {}, "lng", "longitude", -180, 180) ??
      0,
  ];
  const polygons = areaData.length
    ? areaData.flatMap((area) => {
        const latitude = getAreaCoordinate(area, "lat", "latitude", -90, 90);
        const longitude = getAreaCoordinate(
          area,
          "lng",
          "longitude",
          -180,
          180,
        );
        if (latitude === null || longitude === null) {
          if (import.meta.env.DEV)
            console.warn(
              "[LOGIMIND] Skipping area without valid map coordinates:",
              area,
            );
          return [];
        }
        return [
          {
            name: area.name,
            performance: area.performance || "Observed",
            coords: [
              [latitude - 0.009, longitude - 0.008],
              [latitude + 0.009, longitude],
              [latitude, longitude + 0.009],
              [latitude - 0.009, longitude + 0.004],
            ],
            info: `Deliveries: ${area.deliveries ?? "n/a"} • Average duration: ${area.average_delivery_time ?? "n/a"} min`,
          },
        ];
      })
    : [];

  return (
    <div className="relative h-[420px] w-full overflow-hidden rounded-xl border border-slate-200">
      <MapContainer
        center={center}
        zoom={12}
        scrollWheelZoom
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {hubLatitude !== null && hubLongitude !== null && (
          <Marker position={[hubLatitude, hubLongitude]} icon={blueIcon}>
            <Popup>{hubLocation?.name || "Business hub"}</Popup>
          </Marker>
        )}

        {polygons.map((polygon, index) => (
          <AreaPolygon key={`${polygon.name}-${index}`} {...polygon} />
        ))}
      </MapContainer>
      <MapLegend />
    </div>
  );
}
