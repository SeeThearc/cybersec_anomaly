import axios from "axios";

// Setup Axios instance pointing to FastAPI backend
const API_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// --- API Methods ---

export const getStatistics = async () => {
  const response = await api.get("/statistics");
  return response.data;
};

export const getAlerts = async (limit = 100) => {
  const response = await api.get(`/alerts?limit=${limit}`);
  return response.data;
};

export const getEvents = async (limit = 100) => {
  const response = await api.get(`/events?limit=${limit}`);
  return response.data;
};

export const getAnalytics = async () => {
  const response = await api.get("/analytics");
  return response.data;
};

export const runPrediction = async (event) => {
  const response = await api.post("/predict", { event });
  return response.data;
};

export const askCopilot = async (question) => {
  const response = await api.post("/copilot", { question });
  return response.data;
};

export default api;
