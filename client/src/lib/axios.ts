import axios from "axios";

const api = axios.create({
  baseURL: process.env.NODE_ENV === "development" ? process.env.NEXT_PUBLIC_GENSHIN_SETTING_CALCULATOR_API_DEV : process.env.NEXT_PUBLIC_GENSHIN_SETTING_CALCULATOR_API,
});

export default api;
