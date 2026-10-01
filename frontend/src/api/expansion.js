import api from "./client";

export const getExpansion = (businessType) =>
  api.get("/expansion", { params: { business_type: businessType } });
