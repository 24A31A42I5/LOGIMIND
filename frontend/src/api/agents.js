import api from "./client";

export const getAgents = () => api.get("/delivery-agents");
export const getAgentById = (id) => api.get(`/delivery-agents/${id}`);
