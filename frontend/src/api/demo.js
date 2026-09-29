import api from "./client";

export const resetDemo = () => api.post("/day/reset");
export const loadDay = (day) => api.post("/day/load", { day });
export const triggerAreaCDelay = () => api.post("/day/trigger-delay");
export const triggerFailedDeliveryHotspot = () =>
  api.post("/day/trigger-failure");
export const triggerSuccessfulIntervention = () =>
  api.post("/day/trigger-intervention");
export const closeDay = () => api.post("/day/close");
