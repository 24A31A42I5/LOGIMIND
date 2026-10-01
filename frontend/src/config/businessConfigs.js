import distributorConfig from "./distributorConfig";
import restaurantConfig from "./restaurantConfig";
import rawMaterialConfig from "./rawMaterialConfig";
import retailConfig from "./retailConfig";
import serviceProviderConfig from "./serviceProviderConfig";

const shared = {
  common: [
    { to: "/ai-analyzer", label: "AI Analyzer" },
    { to: "/expansion", label: "Expansion" },
    { to: "/memory", label: "Memory" },
  ],
};

export const businessConfigs = {
  distributor: {
    ...distributorConfig,
    label: "Distributor",
    navigation: [
      { to: "/shipments", label: "Shipments" },
      { to: "/delivery-agents", label: "Delivery Agents" },
      { to: "/analytics", label: "Analytics" },
      ...shared.common,
    ],
    metrics: [
      "Shipments",
      "Delivery Activity",
      "Delivery Agents",
      "Operational Hotspots",
    ],
  },
  restaurant: {
    ...restaurantConfig,
    label: "Restaurant",
    navigation: [
      { to: "/orders", label: "Orders" },
      { to: "/sales", label: "Sales" },
      { to: "/analytics", label: "Analytics" },
      { to: "/hotspots", label: "Hotspots" },
      ...shared.common,
    ],
    metrics: ["Orders", "Revenue", "Customer Demand", "Popular Areas"],
  },
  raw_material: {
    ...rawMaterialConfig,
    label: "Raw Material Supplier",
    navigation: [
      { to: "/supplies", label: "Supplies" },
      { to: "/customers", label: "Customers" },
      { to: "/demand", label: "Demand" },
      { to: "/analytics", label: "Analytics" },
      ...shared.common,
    ],
    metrics: ["Supply Volume", "B2B Demand", "Customers", "Supply Areas"],
  },
  retail: {
    ...retailConfig,
    label: "Retail Store",
    navigation: [
      { to: "/sales", label: "Sales" },
      { to: "/products", label: "Products" },
      { to: "/customers", label: "Customers" },
      { to: "/analytics", label: "Analytics" },
      ...shared.common,
    ],
    metrics: ["Sales", "Products", "Customers", "Product Demand"],
  },
  service_provider: {
    ...serviceProviderConfig,
    label: "Service Provider",
    navigation: [
      { to: "/bookings", label: "Bookings" },
      { to: "/customers", label: "Customers" },
      { to: "/service-areas", label: "Service Areas" },
      { to: "/analytics", label: "Analytics" },
      ...shared.common,
    ],
    metrics: ["Bookings", "Customers", "Service Areas", "Appointment Demand"],
  },
};

export const getBusinessConfig = (businessType) =>
  businessConfigs[businessType] || businessConfigs.distributor;
