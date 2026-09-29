import api from "./client";

export const getOverallAnalytics = () => api.get("/analytics/overall");
export const getDailyAnalytics = () => api.get("/analytics/daily");
export const getMonthlyAnalytics = () => api.get("/analytics/monthly");
export const getAreaAnalytics = () => api.get("/analytics/areas");
export const getHotspots = () => api.get("/analytics/hotspots");
export const getTrends = () => api.get("/analytics/trends");
