import api from "./client";

export const getProfile = (userId) =>
  api.get(`/profile/${encodeURIComponent(userId)}`);
export const saveProfile = (profile) => api.put("/profile", profile);
