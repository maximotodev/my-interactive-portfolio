// frontend/src/api/index.js
import axios from "axios";

// This is the key change.
// import.meta.env.VITE_API_BASE_URL is a special variable that Vite
// will replace with the value of an environment variable at build time.
// If that variable doesn't exist (like in local development), it falls back
// to the local Django server's address.
const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${API_URL}/api/`,
});

// All your export functions remain exactly the same
export const fetchProjects = () => API.get("projects/");
export const fetchCertifications = () => API.get("certifications/");
export const fetchGithubStats = () => API.get("github-stats/");
export const fetchGithubContributions = () => API.get("github-contributions/");
export const fetchNostrProfile = () => API.get("nostr-profile/");
export const fetchLatestNote = () => API.get("latest-note/");
export const fetchBitcoinAddress = () => API.get("bitcoin-address/");
export const matchSkills = (query) => API.post("skill-match/", { query });
