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
      className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md hover:shadow-xl dark:ring-1 dark:ring-white/10 dark:hover:bg-gray-700"
    >
      <h3 className="font-bold text-purple-600 dark:text-purple-400">
        GitHub Stats
      </h3>
      <p className="text-gray-700 dark:text-gray-300">
        {stats.public_repos} Repos
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        {stats.followers} Followers
      </p>
      <p className="text-gray-700 dark:text-gray-300">
        {stats.total_stars} Stars
      </p>
    </a>
  );
};

export default GithubStats;
