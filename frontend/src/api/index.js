// frontend/src/api/index.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${API_URL}/api/`,
});

// --- MODIFIED: fetchProjects now accepts an optional tag slug ---
export const fetchProjects = (tagSlug = null) => {
  let url = "projects/";
  if (tagSlug) {
    url += `?tag=${tagSlug}`;
  }
  return API.get(url);
};

// --- NEW: A function to fetch all available tags ---
export const fetchTags = () => API.get("tags/");

export const fetchCertifications = () => API.get("certifications/");
export const fetchGithubStats = () => API.get("github-stats/");
export const fetchGithubContributions = () => API.get("github-contributions/");
export const fetchNostrProfile = () => API.get("nostr-profile/");
export const fetchLatestNote = () => API.get("latest-note/");
export const fetchBitcoinAddress = () => API.get("bitcoin-address/");
export const fetchPosts = () => API.get("posts/");
export const fetchPostBySlug = (slug) => API.get(`posts/${slug}/`);
export const fetchMempoolStats = () => API.get("mempool-stats/");
export const postChatMessage = (question, history) =>
  API.post("chat/", { question, history });
export const matchSkills = (query) => API.post("skill-match/", { query });
