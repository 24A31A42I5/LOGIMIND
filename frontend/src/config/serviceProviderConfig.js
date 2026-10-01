export default {
  id: "service_provider",
  label: "Service Provider",
  operationalEndpoint: "/service-provider/bookings",
  expansionFactors: [
    "demand",
    "customer_density",
    "coverage_gap",
    "operational_feasibility",
  ],
};
