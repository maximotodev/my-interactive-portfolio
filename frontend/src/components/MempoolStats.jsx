// frontend/src/components/MempoolStats.jsx
import React, { useState, useEffect } from "react";
import { fetchMempoolStats } from "../api";
import FadeIn from "./FadeIn";
// Using FaBolt and FaMugHot for better visual distinction
import { FaCube, FaBolt, FaDollarSign, FaMugHot } from "react-icons/fa6";

// A reusable sub-component for our stat cards with dark variants
const StatCard = ({
  icon,
  title,
  value,
  subtext,
  color = "text-gray-900 dark:text-white",
}) => (
  <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md ring-1 ring-black/5 dark:ring-white/10 flex items-center space-x-4">
    <div className={`text-3xl ${color}`}>{icon}</div>
    <div>
      <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
      {subtext && <p className="text-xs text-gray-500">{subtext}</p>}
    </div>
  </div>
);

const MempoolStats = () => {
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const formatHashrate = (hashesPerSecond) => {
    if (!hashesPerSecond || typeof hashesPerSecond !== "number") return "N/A";
    const exahashes = hashesPerSecond / 1e18;
    return `${exahashes.toFixed(2)} EH/s`;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data } = await fetchMempoolStats();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch network stats:", error);
      } finally {
        if (isLoading) setIsLoading(false);
      }
    };
    fetchData();
    const intervalId = setInterval(fetchData, 30000);
    return () => clearInterval(intervalId);
  }, [isLoading]);

  if (isLoading) {
    return (
      <div className="h-40 animate-pulse bg-gray-200 dark:bg-gray-800 rounded-lg my-12"></div>
    );
  }

  if (!stats) return null;

  const { recommended_fees, block_height, hashrate, price } = stats;

  return (
    <FadeIn>
      <section className="my-12">
        <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2 text-gray-900 dark:text-gray-100">
          Live Bitcoin Network Status
        </h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            icon={<FaCube />}
            title="Latest Block"
            value={block_height.toLocaleString()}
            color="text-yellow-600 dark:text-yellow-400"
          />
          <StatCard
            icon={<FaMugHot />}
            title="Network Hashrate"
            value={formatHashrate(hashrate)}
            // Default text color will be used here
          />
          <StatCard
            icon={<FaDollarSign />}
            title="Price (USD)"
            value={price ? `$${price.toLocaleString()}` : "N/A"}
            color="text-green-600 dark:text-green-400"
          />
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg ring-1 ring-black/5 dark:ring-white/10 col-span-2 lg:col-span-1 shadow-md">
            <div className="flex items-center space-x-4">
              <div className="text-3xl text-purple-600 dark:text-purple-400">
                <FaBolt />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Transaction Fees
                </p>
                <p className="text-lg font-bold text-gray-800 dark:text-gray-200">
                  sat/vB
                </p>
              </div>
            </div>
            <div className="space-y-2 mt-3 text-sm text-gray-700 dark:text-gray-300">
              {/* Changed color order to be more intuitive: High=Red, Low=Green */}
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                  High Priority
                </span>
                <strong>{recommended_fees.fastestFee}</strong>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
                  Medium Priority
                </span>
                <strong>{recommended_fees.halfHourFee}</strong>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                  Low Priority
                </span>
                <strong>{recommended_fees.economyFee}</strong>
              </div>
            </div>
          </div>
        </div>
      </section>
    </FadeIn>
  );
};

export default MempoolStats;
