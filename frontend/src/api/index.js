// frontend/src/api/index.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${API_URL}/api/`,
});

export const fetchProjects = () => API.get("projects/");
export const fetchCertifications = () => API.get("certifications/");
export const fetchGithubStats = () => API.get("github-stats/");
export const fetchGithubContributions = () => API.get("github-contributions/");
export const fetchNostrProfile = () => API.get("nostr-profile/");
export const fetchLatestNote = () => API.get("latest-note/");
export const fetchBitcoinAddress = () => API.get("bitcoin-address/");
export const fetchPosts = () => API.get("posts/");
export const fetchPostBySlug = (slug) => API.get(`posts/${slug}/`);
// The 'matchSkills' export has been removed.
