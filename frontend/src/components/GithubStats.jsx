// frontend/src/components/GithubStats.jsx
import React, { useState, useEffect } from "react";
import { fetchGithubStats } from "../api";
import LoadingSpinner from "./LoadingSpinner";

const GithubStats = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const getStats = async () => {
      try {
        const { data } = await fetchGithubStats();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch GitHub stats:", error);
      }
    };
    getStats();
  }, []);

  if (!stats) return <LoadingSpinner />;

  return (
    <a
      href="https://github.com/maximotodev"
      target="_blank"
      rel="noopener noreferrer"
      className="bg-gray-800 p-4 rounded-lg text-center hover:bg-gray-700 transition-colors"
    >
      <h3 className="font-bold text-purple-400">GitHub Stats</h3>
      <p>{stats.public_repos} Repos</p>
      <p>{stats.followers} Followers</p>
      <p>{stats.total_stars} Stars</p>
    </a>
  );
};

export default GithubStats;
