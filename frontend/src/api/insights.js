import api from "./client";

export const getTodayInsights = () => api.get("/insights/today");
export const investigateArea = (area) =>
  api.post("/insights/investigate", { area });
export const applyRecommendation = (recommendationId) =>
  api.post(`/recommendations/${recommendationId}/apply`);
export const recordRecommendationOutcome = (
  recommendationId,
  beforeMinutes,
  afterMinutes,
) =>
  api.post(`/recommendations/${recommendationId}/outcome`, {
    before_minutes: beforeMinutes,
    after_minutes: afterMinutes,
  });
