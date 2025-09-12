// frontend/src/api/index.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${API_URL}/api/`,
});
export const fetchProducts = async (page = 1, { signal } = {}) => {
  try {
    // Correct endpoint is /products/
    const response = await API.get(`products/?page=${page}`, { signal });
    return response.data;
  } catch (err) {
    if (!axios.isCancel(err)) {
      console.error("Error fetching products:", err);
    }
    return { count: 0, results: [] };
  }
};

export const performSearch = (query) => API.get(`search/?q=${query}`);

export const fetchProjects = (tagSlug = null, { signal } = {}) => {
  let url = "projects/";
  if (tagSlug) {
    url += `?tag=${tagSlug}`;
  }
  return API.get(url, { signal }); // Pass the signal to axios
};
export const fetchTags = ({ signal }) => API.get("tags/", { signal }); // Accept the signal

export const fetchCertifications = ({ signal } = {}) =>
  API.get("certifications/", { signal });

export const fetchGithubStats = () => API.get("github-stats/");
export const fetchGithubContributions = () => API.get("github-contributions/");
export const fetchNostrProfile = (pubkey = null) => {
  let url = "nostr-profile/";
  if (pubkey) {
    // We'll send the pubkey as a query parameter.
    url += `?pubkey=${pubkey}`;
  }
  return API.get(url);
};
export const fetchLatestNote = () => API.get("latest-note/");
export const fetchBitcoinAddress = () => API.get("bitcoin-address/");
export const fetchPosts = ({ signal } = {}) => API.get("posts/", { signal });
export const fetchPostBySlug = (slug) => API.get(`posts/${slug}/`);
export const fetchMempoolStats = () => API.get("mempool-stats/");
export const postChatMessage = (question, history) =>
  API.post("chat/", { question, history });
export const matchSkills = (query) => API.post("skill-match/", { query });
export const submitContactForm = (formData) => API.post("contact/", formData);
export const submitNostrContactForm = (formData) =>
  API.post("nostr-contact/", formData);
