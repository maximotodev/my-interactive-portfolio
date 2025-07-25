// frontend/src/components/MempoolStats.jsx
import React, { useState, useEffect } from "react";
import { fetchMempoolStats } from "../api"; // Only need this one now
import FadeIn from "./FadeIn";
import { FaCube, FaBolt, FaDollarSign, FaMugHot } from "react-icons/fa6";

const StatCard = ({ icon, title, value, subtext, color = "text-white" }) => (
  <div className="bg-gray-800 p-6 rounded-lg flex items-center space-x-4 ring-1 ring-white/10">
    <div className={`text-3xl ${color}`}>{icon}</div>
    <div>
      <p className="text-sm text-gray-400">{title}</p>
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
        // --- SIMPLIFIED LOGIC ---
        // Only one API call is needed now
        const { data } = await fetchMempoolStats();
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch network stats:", error);
      } finally {
        if (isLoading) setIsLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 30000); // Polls every 30 seconds
    return () => clearInterval(intervalId);
  }, [isLoading]);

  if (isLoading) {
    return (
      <div className="h-40 animate-pulse bg-gray-800 rounded-lg my-12"></div>
    );
  }

  if (!stats) return null;

  const { recommended_fees, block_height, hashrate, price } = stats;

  return (
    <FadeIn>
      <section className="my-12">
        <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2">
          Live Bitcoin Network Status
        </h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            icon={<FaCube />}
            title="Latest Block"
            value={block_height.toLocaleString()}
            color="text-yellow-400"
          />
          <StatCard
            icon={<FaMugHot />}
            title="Network Hashrate"
            value={formatHashrate(hashrate)}
          />
          <StatCard
            icon={<FaDollarSign />}
            title="Price (USD)"
            // The price now comes from the 'stats' object
            value={price ? `$${price.toLocaleString()}` : "N/A"}
            color="text-green-400"
          />
          <div className="bg-gray-800 p-6 rounded-lg ring-1 ring-white/10 col-span-2 lg:col-span-1">
            <div className="flex items-center space-x-4">
              <div className="text-3xl text-purple-400">
                <FaBolt />
              </div>
              <div>
                <p className="text-sm text-gray-400">Transaction Fees</p>
                <p className="text-lg font-bold">sat/vB</p>
              </div>
            </div>
            <div className="space-y-2 mt-3 text-sm">
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                  High Priority
                </span>{" "}
                <strong>{recommended_fees.fastestFee}</strong>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
                  Medium Priority
                </span>{" "}
                <strong>{recommended_fees.halfHourFee}</strong>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                  Low Priority
                </span>{" "}
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
