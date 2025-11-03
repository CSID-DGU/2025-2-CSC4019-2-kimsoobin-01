import axios from "axios";

// 백엔드 프록시(vite.config.js) 덕분에 /v1 로 바로 호출 가능
export const api = axios.create({
  baseURL: "/",
  timeout: 30000
});
