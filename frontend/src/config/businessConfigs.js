import distributorConfig from "./distributorConfig";
import restaurantConfig from "./restaurantConfig";
import rawMaterialConfig from "./rawMaterialConfig";
import retailConfig from "./retailConfig";
import serviceProviderConfig from "./serviceProviderConfig";

const shared = {
  common: [
    { to: "/ai-analyzer", label: "AI Operations Analyst" },
    { to: "/expansion", label: "Expansion Intelligence" },
    { to: "/memory", label: "Memory" },
  ],
};

export const businessConfigs = {
  distributor: {
    ...distributorConfig,
    label: "Distributor",
    navigation: [
      { to: "/shipments", label: "Shipments & Orders" },
      { to: "/delivery-agents", label: "Delivery Agents" },
      { to: "/analytics", label: "Performance Analytics" },
      ...shared.common,
    ],
    metrics: [
      "Total orders and shipments",
      "On-time delivery rate",
      "Average delivery duration",
      "Delayed and failed deliveries",
    ],
  },
  restaurant: {
    ...restaurantConfig,
    label: "Restaurant",
    navigation: [
      { to: "/orders", label: "Orders" },
      { to: "/sales", label: "Sales & Costs" },
      { to: "/analytics", label: "Menu Performance" },
      { to: "/hotspots", label: "Kitchen Operations" },
      ...shared.common,
    ],
    metrics: [
      "Orders received and completed",
      "Average order preparation time",
      "Revenue and average order value",
      "Food cost percentage",
    ],
  },
  raw_material: {
    ...rawMaterialConfig,
    label: "Raw Material Supplier",
    navigation: [
      { to: "/supplies", label: "Purchase Orders" },
      { to: "/customers", label: "Suppliers" },
      { to: "/demand", label: "Raw Material Inventory" },
      { to: "/analytics", label: "Fulfillment & Lead Times" },
      ...shared.common,
    ],
    metrics: [
      "Open purchase orders",
      "Available material stock",
      "Supplier on-time rate",
      "Average procurement lead time",
    ],
  },
  retail: {
    ...retailConfig,
    label: "Retail Store",
    navigation: [
      { to: "/sales", label: "Sales" },
      { to: "/products", label: "Products & Categories" },
      { to: "/customers", label: "Inventory & Replenishment" },
      { to: "/analytics", label: "Store Performance" },
      ...shared.common,
    ],
    metrics: [
      "Sales revenue",
      "Transactions",
      "Average basket value",
      "Gross margin",
    ],
  },
  service_provider: {
    ...serviceProviderConfig,
    label: "Service Provider",
    navigation: [
      { to: "/bookings", label: "Service Requests" },
      { to: "/customers", label: "Customers & Service History" },
      { to: "/service-areas", label: "Technicians & Scheduling" },
      { to: "/analytics", label: "SLA Performance" },
      ...shared.common,
    ],
    metrics: [
      "Open service requests",
      "Completed work orders",
      "Average resolution time",
      "SLA compliance",
    ],
  },
};

export const getBusinessConfig = (businessType) =>
  businessConfigs[businessType] || businessConfigs.distributor;
