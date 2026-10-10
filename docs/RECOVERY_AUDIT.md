# LOGIMIND recovery audit

## Current architecture

The repository is a FastAPI + MongoDB backend and a React + Vite frontend. The backend is organized around a single app entry point in `backend/main.py` and multiple domain modules under `backend/domains/*`. The current shape is:

- Frontend routes under `frontend/src` for onboarding, profile setup, dashboard, map, AI analysis, memory, expansion, and domain workspaces.
- Backend routers in `backend/routers/*` for auth, analytics, insight, recommendation, memory, expansion, import, shipment, and delivery-agent flows.
- Domain services in `backend/domains/<domain>/service.py` and `backend/domains/<domain>/routes.py` for distributor, restaurant, raw_material, retail, and service_provider.
- Shared orchestration in `backend/common/ai/*` and `backend/common/analytics/*`.
- Data access in `backend/common/repository.py`, `backend/core/database.py`, and `backend/config/database.py`.
- AI/Hindsight integration in `backend/services/llmService.py`, `backend/services/hindsightService.py`, and `backend/config/*.py`.
- Synthetic demo data in `backend/services/seedService.py` and related `backend/data/*.json` assets.

## Duplicate implementations

The repository has overlapping responsibilities across multiple layers:

- Analytics orchestration is duplicated between `backend/services/analyticsService.py` and `backend/common/analytics/analyticsService.py`.
- Intelligence orchestration is split between `backend/common/ai/intelligenceService.py` and `backend/services/recommendationService.py`.
- Recommendation generation is duplicated across `backend/common/ai/recommendationService.py` and `backend/services/llmService.py`.
- Hindsight memory logic is implemented in `backend/services/hindsightService.py` and `backend/common/memory/hindsightService.py`.
- Domain metrics are implemented by both per-domain service modules and generic analytics helpers.

## Dead code

- Several files appear to be legacy scaffolding or historical prototypes, especially in `backend/common/` and `backend/services/` where similar responsibilities are redundantly implemented.
- Some routes and controllers remain unused in the active flow or are only connected to demo-only behavior.
- A number of files appear disconnected from the main request path without a clear owner in the live architecture.

## Broken wiring

- The application relies on multiple data sources and layers without a single authoritative owner for analytics and recommendation flow.
- The LLM service reads `LLM_API_KEY` while the project examples and environment docs route configuration through `GROQ_API_KEY` and different provider semantics.
- Hindsight auth headers are effectively invalid because the API key is not passed in the correct bearer format.
- The system often returns synthetic demo data as if it were live operational intelligence.
- Some analysis outputs do not carry an explicit `data_source` or evidence identifier and therefore cannot distinguish live from synthetic data.

## Fake/demo behavior

- Demo operations are seeded through `backend/services/seedService.py` and `backend/controllers/demoController.py`.
- Several domain services call `read_domain_records(...)` with seed data and mark records as `synthetic=True` without explicitly surfacing the source in the recommendation pipeline.
- Recommendation and memory flows sometimes accept demo fallback output as if it were production-grade intelligence.

## Missing behavior

- The distributor vertical slice is partly implemented but not fully wired to a single evidence-driven recommendation loop.
- A real recommendation must include actual evidence, historical context, proposed action, expected impact, confidence, and the data source.
- `Apply Recommendation` does not yet mutate the underlying operational state in a meaningful way; it mostly records a click or an intervention object.
- The AI decision path does not consistently preserve contextual evidence for live distributor records such as Area C evening delay detection.

## Security issues

- Several services build outbound HTTP requests with malformed or redacted authorization values, which prevents legitimate authenticated calls and can hide configuration drift.
- The codebase has a pattern of trusting local, demo, or synthetic data without clearly marking it as such.
- Some APIs do not clearly distinguish authenticated live data from demo-only records.

## Missing tests

No Python test suite is present in the repository for the backend business logic. There are no tests covering:

- distributor delay detection
- recommendation generation
- outcome recording
- recommendation application
- domain data source labeling
- auth boundary enforcement

## Recommended ownership

- `domains/distributor/`: owns distributor operational records, area metrics, delay patterns, and execution outcomes.
- `domains/restaurant/`: owns restaurant volume, demand, staffing, and service-window metrics.
- `domains/retail/`: owns retail demand density, sales patterns, and coverage analysis.
- `domains/raw_material/`: owns supply reliability, volume, and industrial coverage metrics.
- `domains/service_provider/`: owns booking density, resource load, and provider scheduling patterns.
- `backend/common/analytics/`: owns shared metric normalization and aggregation primitives.
- `backend/common/ai/`: owns the shared intelligence flow and recommendation composition.
- `backend/services/`: owns external integrations (LLM, Hindsight, seeding, rebuild utilities) and environment-specific glue.
- `backend/controllers/`: owns request orchestration and state changes after domain logic has produced the authoritative outcome.

The project should keep the multi-domain architecture but narrow each domain to its own operational evidence and maintain a single shared contract for analytics, intelligence, recommendations, actions, and outcomes.
