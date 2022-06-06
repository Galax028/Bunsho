import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.MODE === "production"
      ? `${window.location.origin}/api`
      : "http://localhost:8000/api",
});

export default api;
