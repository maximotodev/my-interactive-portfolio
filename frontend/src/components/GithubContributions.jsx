// frontend/src/components/GithubContributions.jsx
import React, { useState, useEffect } from "react";
import GitHubCalendar from "react-github-calendar";
import { fetchGithubContributions } from "../api";
import LoadingSpinner from "./LoadingSpinner";

const GithubContributions = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getContributions = async () => {
      try {
        const response = await fetchGithubContributions();
        setData(response.data);
      } catch (error) {
        console.error("Failed to fetch GitHub contributions:", error);
      } finally {
        setLoading(false);
      }
    };
    getContributions();
  }, []);

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md h-48 flex items-center justify-center animate-pulse">
        <LoadingSpinner />
      </div>
    );
  }

  if (!data) {
    return (
      <p className="text-center text-red-400">
        Could not load contribution data.
      </p>
    );
  }

  // The API returns weeks, but the component needs a flat array of days.
  // We can flatten the data structure here.
  const contributions = data.weeks.reduce((acc, week) => {
    return [...acc, ...week.contributionDays];
  }, []);

  // The library expects a specific data format. We transform our API data into it.
  const transformData = (contribs) => {
    return contribs.map((day) => ({
      date: day.date,
      count: day.contributionCount,
      level: Math.min(day.contributionCount, 4), // The library expects levels 0-4
    }));
  };

  return (
    <section className="my-12">
      <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2 text-gray-900 dark:text-gray-100">
        {data.totalContributions} Contributions in the Last Year
      </h2>
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg text-gray-800 dark:text-gray-200 ring-1 ring-black/5 dark:ring-white/10">
        <GitHubCalendar
          username="maximotodev"
          data={transformData(contributions)}
          // The component's built-in 'dark' theme works perfectly with our toggle
          theme={{
            light: ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
            dark: ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
          }}
          blockSize={14}
          blockMargin={4}
          fontSize={16}
          hideTotalCount
          hideColorLegend
        />
      </div>
    </section>
  );
};

export default GithubContributions;
