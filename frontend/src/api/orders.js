import api from "./client";

export const getRestaurantOrders = () => api.get("/restaurant/orders");
