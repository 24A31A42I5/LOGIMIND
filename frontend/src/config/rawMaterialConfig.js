export default {
  id: "raw_material",
  label: "Raw Material Supplier",
  operationalEndpoint: "/raw-material/supplies",
  expansionFactors: [
    "demand",
    "customer_density",
    "coverage_gap",
    "operational_feasibility",
  ],
};
