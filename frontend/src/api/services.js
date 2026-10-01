import api from "./client";

export const getServiceBookings = () => api.get("/service-provider/bookings");
export const getRawMaterialSupplies = () => api.get("/raw-material/supplies");
export const getRetailSales = () => api.get("/retail/sales");
