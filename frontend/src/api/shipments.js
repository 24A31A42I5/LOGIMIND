import api from "./client";

export const getShipments = (params = {}) => api.get("/shipments", { params });
export const getShipmentById = (id) => api.get(`/shipments/${id}`);
