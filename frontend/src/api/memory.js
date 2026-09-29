import api from "./client";

export const getRecentMemory = () => api.get("/memory/recent");
export const recallMemory = (query) => api.post("/memory/recall", { query });
export const reflectMemory = (context) =>
  api.post("/memory/reflect", { context });
export const getMemoryStats = () => api.get("/memory/stats");
