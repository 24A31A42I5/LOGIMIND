# FRONTEND DOMAIN AUDIT

## Scope
This audit inspects the actual frontend code in the LOGIMIND repository before changing behavior. The goal was to verify whether the current web app is a single generic dashboard disguised as multiple domains or a genuine multi-domain BI shell.

## Actual frontend structure

### Routing and application shell
- Entry point: `frontend/src/App.jsx`
- Route configuration: `frontend/src/routes.jsx`
- Auth/business shell container: `frontend/src/components/layout/Shell.jsx`
- Sidebar navigation: `frontend/src/components/layout/Sidebar.jsx`
- Domain switcher/business profile state: `frontend/src/context/BusinessContext.jsx`

### Domain registry and configuration
- Business type registry: `frontend/src/config/businessTypes.js`
- Business configuration map: `frontend/src/config/businessConfigs.js`
- Domain configs:
  - `frontend/src/config/distributorConfig.js`
  - `frontend/src/config/restaurantConfig.js`
  - `frontend/src/config/rawMaterialConfig.js`
  - `frontend/src/config/retailConfig.js`
  - `frontend/src/config/serviceProviderConfig.js`

### Key pages
- Welcome/auth: `frontend/src/pages/WelcomePage.jsx`, `frontend/src/pages/LoginPage.jsx`
- Profile setup: `frontend/src/pages/ProfileSetupPage.jsx`
- Shared dashboard shell: `frontend/src/pages/DashboardPage.jsx`
- Domain workspace fallback: `frontend/src/pages/DomainWorkspacePage.jsx`
- AI and expansion areas: `frontend/src/pages/AiAnalyzerPage.jsx`, `frontend/src/pages/ExpansionPage.jsx`

## Actual routing flow
The app is structured as:

1. Welcome / sign-up / sign-in
2. Business profile setup (`/profile-setup`)
3. Shared shell (`/dashboard`, `/shipments`, `/delivery-agents`, `/orders`, `/sales`, etc.)
4. Domain-specific workspace pages under the shared shell

The route table in `frontend/src/routes.jsx` does include the five supported business types:
- distributor
- restaurant
- raw_material
- retail
- service_provider

## Domain selection and persistence
Business profile state is stored in browser local storage under `logimind-profile` and restored in `BusinessContext.jsx`.

Important finding:
- The profile selector in `ProfileSetupPage.jsx` intentionally filtered out the `service_provider` option.
- This means the application was not exposing the full five-domain architecture to the user even though the backend and config registry still included it.
- The app therefore violated the intended domain selection goal and silently reduced the supported domain set.

This is one of the clearest functional bugs in the frontend.

## Shared shell and domain-specific UX
The app already does have a reusable shell architecture, which is good:
- `Shell.jsx` provides the common layout and nav.
- `Sidebar.jsx` reads configured navigation items from the domain config.
- `BusinessContext` resolves the active domain config.

However, the current implementation still uses a generic dashboard shape and generic labels for most domains. The dashboard and workspace presenter are not yet genuinely distinct by domain in a way that matches the business brief:
- `DashboardPage.jsx` mostly derives generic KPI summaries from `config.metrics`.
- `DomainWorkspacePage.jsx` uses mostly generic placeholders instead of a truly distinct operational composition for each domain.
- The domain config labels are partly generic (`Analytics`, `Hotspots`, `Customers`) rather than the domain-specific task lists called out in the brief.

## Frontend API clients and backend endpoints
The frontend calls a centralized Axios client with endpoints grouped by feature:

- `frontend/src/api/client.js` — shared Axios instance and auth-related handling
- `frontend/src/api/analytics.js` — analytics endpoints
- `frontend/src/api/shipments.js` — shipments and delivery data
- `frontend/src/api/agents.js` — delivery agents
- `frontend/src/api/profile.js` — business profile persistence
- `frontend/src/api/insights.js` — insights/recommendations
- `frontend/src/api/expansion.js` — expansion intelligence
- `frontend/src/api/memory.js` — memory timeline
- `frontend/src/api/orders.js` — order data
- `frontend/src/api/services.js` — service-provider data
- `frontend/src/api/demo.js` — demo or sample data access

The endpoint usage pattern is consistent with a shared API layer that expects real backend data, though the app still mixes live endpoints with placeholders and synthetic-warning messaging.

## Live vs synthetic data
The current frontend explicitly surfaces synthetic/demo states in a few places:
- `DashboardPage.jsx` sets and displays `synthetic` state from API responses.
- `DomainRecordsPage.jsx` renders a synthetic-data banner when backend data is marked as demo.
- `DomainWorkspacePage.jsx` shows synthetic warnings when `data.synthetic` is returned.

This is the right overall direction: the UI is already aware of real vs synthetic evidence. The unresolved issue is that the domains and navigation were still not fully aligned with the true domain workload and selection logic.

## Existing tests and commands
There are no frontend test files visible in the repository snapshot. The available verification commands come from `frontend/package.json`:

- `cd frontend && npm run build`
- `cd frontend && npm run lint`
- `cd frontend && npm run dev`

These commands are the realistic validation path for the frontend work.

## Findings
### Working parts
- Shared shell structure is present and reusable.
- Multi-domain registry and route stubs exist.
- Business profile persistence and local storage flow are implemented.
- Live API layer is centralized via Axios.
- Synthetic/live labeling logic already exists in multiple UI surfaces.

### Gaps and broken behavior
1. Service-provider business selection is hidden from the available profile options.
2. The application still presents a generic dashboard pattern and does not yet fully differentiate the five workspaces by their required operational model.
3. Navigation labels and workspace composition remain a bit too uniform for the business brief.
4. The “genuinely domain-specific” requirement still needs stronger config and dashboard materialization rather than just a different label on the same generic layout.

## Approved implementation plan
1. Fix the business-selection bug so all five domains remain selectable.
2. Normalize the domain config and business registry to keep the selected domain valid and consistent with the stored profile.
3. Strengthen the domain-specific navigation labels so each workspace reflects its own operational model.
4. Keep the shared shell, but make the dashboard and workspace views more clearly domain-specific while preserving the common infrastructure.
5. Validate with the existing build/lint commands and keep the domain logic aligned with the real backend data model.
