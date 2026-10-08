import api from "./client";

export const login = (email, password) =>
  api.post("/auth/login", { email, password });
export const signup = (email, password) =>
  api.post("/auth/signup", { email, password });
