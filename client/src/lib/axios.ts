import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_SHH_CALCULATOR_API_URL,
});

export default api;
