# LOGIMIND Frontend

The LOGIMIND frontend is a React/Vite JavaScript application for four business domains:

- Distributor
- Raw material supplier
- Retailer
- Restaurant

It provides authenticated onboarding, browser/device hub geolocation with manual fallback, domain-specific dashboards, Leaflet/OpenStreetMap operational maps, Recharts analytics, CSV import controls, AI analysis review/apply flow, recommendation actions, and Hindsight evidence views.

## Local Development

```powershell
npm install
npm run dev
```

The Vite app expects the backend at `http://localhost:8000/api` by default. Set `VITE_API_BASE_URL` when the backend uses another URL.

## Verification

```powershell
npm run lint
npm run build
```

The repository root [Readme.md](../Readme.md) documents the complete product architecture, backend setup, environment variables, API flow, MongoDB collections, Hindsight behavior, and local run commands.
