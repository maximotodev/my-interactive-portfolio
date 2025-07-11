// frontend/src/api/index.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
});

export const fetchProjects = () => API.get("projects/");
export const fetchCertifications = () => API.get("certifications/");
export const fetchGithubStats = () => API.get("github-stats/");
export const fetchGithubContributions = () => API.get("github-contributions/");
export const fetchNostrProfile = () => API.get("nostr-profile/");
export const fetchLatestNote = () => API.get("latest-note/");
export const fetchBitcoinAddress = () => API.get("bitcoin-address/");
export const matchSkills = (query) => API.post("skill-match/", { query });
