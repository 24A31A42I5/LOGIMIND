import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api/client";
import { getOverallAnalytics } from "../api/analytics";
import { useBusiness } from "../context/useBusiness";

const content = {
  "/orders": [
    "Orders",
    "Track ordering patterns, peak periods, and delivery demand.",
    ["Orders today", "Repeat customers", "Peak period"],
  ],
  "/sales": [
    "Sales",
    "Understand revenue movement and the products or services creating demand.",
    ["Sales today", "Growth trend", "Top category"],
  ],
  "/analytics": [
    "Analytics",
    "Compare current operating signals with the evidence behind expansion decisions.",
    ["Demand trend", "Customer density", "Coverage"],
  ],
  "/hotspots": [
    "Hotspots",
    "See where customer demand is concentrating before choosing an action.",
    ["Strongest area", "Demand signal", "Coverage gap"],
  ],
  "/supplies": [
    "Supplies",
    "Monitor material movement and B2B supply coverage.",
    ["Supply volume", "Open orders", "Delivery areas"],
  ],
  "/customers": [
    "Customers",
    "Understand customer concentration and service opportunities.",
    ["Active customers", "Repeat rate", "Top area"],
  ],
  "/demand": [
    "Demand",
    "Translate business-specific demand into reusable intelligence signals.",
    ["Current demand", "Growth trend", "Demand areas"],
  ],
  "/products": [
    "Products",
    "Track product movement and the demand patterns behind it.",
    ["Products tracked", "Fast movers", "Stock signal"],
  ],
  "/bookings": [
    "Bookings",
    "Understand appointment demand and service capacity.",
    ["Bookings today", "Peak period", "Open requests"],
  ],
  "/service-areas": [
    "Service Areas",
    "Compare service radius, booking demand, and operational reach.",
    ["Active areas", "Coverage gap", "Travel load"],
  ],
};

const domainMetricDefinitions = {
  distributor: [
    ["Deliveries observed", "total_deliveries"],
    ["Delay rate", "delay_rate"],
    ["Average delivery duration", "average_delivery_time"],
  ],
  restaurant: [
    ["Orders observed", "orders"],
    ["Revenue observed", "revenue"],
    ["Average preparation time", "average_preparation_minutes"],
  ],
  retail: [
    ["Transactions observed", "transactions"],
    ["Revenue observed", "revenue"],
    ["Units sold", "units_sold"],
  ],
  raw_material: [
    ["Open purchase orders", "open_orders"],
    ["Available stock", "available_stock"],
    ["Average lead time", "average_lead_time_days"],
  ],
  service_provider: [
    ["Open work orders", "open_work_orders"],
    ["Completed work orders", "completed_work_orders"],
    ["SLA compliance", "sla_compliance_rate"],
  ],
};

function formatMetric(value, key) {
  if (value === null || value === undefined) return "—";
  if (key.includes("rate")) return `${value}%`;
  if (key.includes("revenue")) return `₹${Number(value).toLocaleString()}`;
  if (key.includes("time") || key.includes("lead")) return `${value} ${key.includes("lead") ? "days" : "min"}`;
  return Number(value).toLocaleString();
}

export default function DomainWorkspacePage() {
  const { pathname } = useLocation();
  const { config } = useBusiness();
  const [title, description] =
    content[pathname] || content["/analytics"];
  const [records, setRecords] = useState([]);
  const [state, setState] = useState("loading");
  const [dataSource, setDataSource] = useState("unknown");
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    Promise.all([
      api.get(config.operationalEndpoint),
      getOverallAnalytics(),
    ]).then(([operationsResponse, analyticsResponse]) => {
        const operations = operationsResponse.data;
        const overall = analyticsResponse.data;
        setRecords(operations.records || []);
        setAnalytics(overall);
        setDataSource(overall.data_source || operations.data_source || "unknown");
        setState("ready");
      })
      .catch(() => setState("error"));
  }, [config.operationalEndpoint]);

  const domainMetrics = analytics?.domain_metrics || {};
  const metricDefinitions = domainMetricDefinitions[config.id] || [];
  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">
          {config.label}
        </p>
        <h1 className="mt-1 text-3xl font-bold text-slate-900">{title}</h1>
        <p className="mt-2 text-slate-600">{description}</p>
      </div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        Source: {dataSource === "mongodb" ? "MongoDB operational records" : dataSource}
      </p>
      {state === "error" && (
        <p className="rounded-lg bg-amber-50 p-4 text-amber-800">
          {title} data is unavailable. Check the domain service and try again.
        </p>
      )}
      {state !== "loading" && state !== "error" && (
        <div className="grid gap-4 md:grid-cols-3">
          {metricDefinitions.map(([label, key]) => (
            <div
              key={key}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <p className="text-sm text-slate-500">{label}</p>
              <p className="mt-3 text-3xl font-bold text-slate-900">
                {formatMetric(domainMetrics[key], key)}
              </p>
              <p className="mt-2 text-sm text-slate-600">
                Verified from {records.length} current record{records.length === 1 ? "" : "s"}
              </p>
            </div>
          ))}
        </div>
      )}
      {state === "ready" && records.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-6 text-slate-600">
          No operational records are available for this workspace yet. Import
          records or connect the domain source before requesting analysis.
        </div>
      )}
      {state === "loading" && (
        <p className="text-slate-600">Loading {title.toLowerCase()}...</p>
      )}
    </div>
  );
}
