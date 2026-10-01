export const BUSINESS_TYPES = [
  {
    id: "distributor",
    label: "Distributor",
    description: "Shipments, delivery zones, and hubs",
  },
  {
    id: "restaurant",
    label: "Restaurant",
    description: "Orders, sales, and local demand",
  },
  {
    id: "raw_material",
    label: "Raw Material Supplier",
    description: "B2B supply volume and customers",
  },
  {
    id: "retail",
    label: "Retail Store",
    description: "Products, sales, and customer demand",
  },
  {
    id: "service_provider",
    label: "Service Provider",
    description: "Bookings, service areas, and demand",
  },
];

export const isBusinessType = (value) =>
  BUSINESS_TYPES.some((type) => type.id === value);
