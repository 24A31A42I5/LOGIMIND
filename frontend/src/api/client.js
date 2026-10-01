import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 20000,
});
api.interceptors.request.use((config) => {
  let user = null;
  try {
    user = JSON.parse(localStorage.getItem("logimind-user") || "null");
  } catch {
    localStorage.removeItem("logimind-user");
  }
  if (user?.access_token)
    config.headers.Authorization = `Bearer ${user.access_token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("logimind-user");
      localStorage.removeItem("logimind-profile");
    }
    return Promise.reject(error);
  },
);

export default api;
