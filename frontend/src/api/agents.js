import api from "./client";

export const getAgents = () => api.get("/delivery-agents");
export const getAgentById = (id) => api.get(`/delivery-agents/${id}`);
export const getAgentLocations = () => api.get("/delivery-agents/locations");
export const updateAgentLocation = (id, location) =>
  api.post(`/delivery-agents/${id}/location`, location);
