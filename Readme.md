# LOGIMIND V2

LOGIMIND is an AI-powered multi-domain business operations intelligence platform for:

- Distributors
- Raw material suppliers
- Retail stores
- Restaurants
- Service providers

It combines current operational records, validation, analytics, geospatial evidence, AI interpretation, recommendations, user actions, outcomes, and Hindsight memory. It is an operations intelligence workspace, not a generic chatbot or BI dashboard.

## Architecture

- **Frontend:** React, Vite, JavaScript/JSX, React Router, Tailwind CSS, Leaflet/OpenStreetMap, Recharts, Axios
- **Backend:** FastAPI, Python, Pydantic, MongoDB
- **Operational data:** MongoDB collections scoped by `userId` and business type. Empty or unavailable MongoDB is reported explicitly; operational APIs never seed or synthesize records.
- **AI:** configurable provider/model through `LLM_PROVIDER`, `LLM_MODEL`, and provider credentials
- **Long-term memory:** Hindsight API for scoped recall and retention of meaningful operational experiences

The shared flow is:

`Operational data -> validation -> analytics -> AI analysis -> insight -> recommendation -> action -> outcome -> Hindsight memory`

## User Flow

1. Open the welcome page.
2. Sign up or sign in.
3. Choose one of the five business domains.
4. Set a business name and hub. Browser geolocation is requested; manual latitude/longitude entry remains available when permission is denied or unavailable.
5. Use the domain dashboard, analytics, AI analysis, map, recommendations, and memory views.

## Analytics and Maps

Analytics support today, week, month, and overall periods. Hotspot and lowspot candidates are calculated from operational records and their coordinates. The LLM interprets calculated evidence; it does not create coordinates or statistics.

`Run AI Analysis` creates a versioned analysis record. The result is shown separately from the current map. `Update Map` applies the selected analysis, updates the saved analysis status, and attempts to retain the meaningful event in Hindsight.

Maps show the saved business hub and observed operational locations. Empty datasets produce an empty state rather than fabricated map regions.

## API Highlights

- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET /api/profile/{user_id}` and `PUT /api/profile`
- `GET /api/analytics/{overall,daily,monthly,areas,hotspots,trends}`
- `POST /api/analysis` with `today`, `week`, `month`, or `overall`
- `POST /api/analysis/{analysis_id}/apply`
- Domain operation endpoints under `/api/distributor`, `/api/restaurant`, `/api/raw-material`, and `/api/retail`
- Existing recommendation, insight, expansion, memory, shipment, and delivery-agent routes remain available and authenticated where applicable.

All protected routes derive identity from the bearer token. Frontend-supplied user IDs are not trusted for profile access.

## Environment

Create `backend/.env` from `backend/.env.example` and configure the services you use:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=logimind
LOGIMIND_AUTH_SECRET=change-this-in-production
FRONTEND_URL=http://localhost:5173
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=
HINDSIGHT_API_URL=
HINDSIGHT_API_KEY=
HINDSIGHT_BANK_ID=
```

The application keeps authentication and profile setup usable when optional services are unavailable. Operational reads and writes require MongoDB and return an explicit `503` when it cannot provide authoritative records. The LLM and Hindsight integrations report unavailable capabilities; they never fabricate evidence, memories, coordinates, or outcomes.

## Run Locally

Backend on Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Verification

```powershell
cd backend
python -m pytest -q

cd ..\frontend
npm run lint
npm run build
```

CSV import is the supported development and production ingestion path. Demo and seed utilities are not mounted by the API and must not be used as operational evidence. Imported records retain their authenticated `userId` and domain type.
