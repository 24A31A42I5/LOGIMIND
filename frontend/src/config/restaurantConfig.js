export default {
  id: "restaurant",
  label: "Restaurant",
  operationalEndpoint: "/restaurant/orders",
  expansionFactors: [
    "demand",
    "customer_density",
    "foot_traffic",
    "coverage_gap",
  ],
};
