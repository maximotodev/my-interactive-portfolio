import React from "react";
import FadeIn from "../components/FadeIn";
import GithubStats from "../components/GithubStats";
import GithubContributions from "../components/GithubContributions";
import MempoolStats from "../components/MempoolStats";
import LatestNostrNote from "../components/LatestNostrNote";

const Dashboard = () => {
  return (
    <div className="container mx-auto p-4 md:p-8 max-w-5xl">
      <FadeIn>
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">
            Live Dashboard
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">
            A real-time overview of my digital footprint and the Bitcoin
            network.
          </p>
        </header>
      </FadeIn>

      <main className="space-y-12">
        <FadeIn delay={200}>
          <MempoolStats />
        </FadeIn>

        <FadeIn delay={300}>
          <GithubContributions />
        </FadeIn>

        <FadeIn delay={400}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <GithubStats />
            <LatestNostrNote />
          </div>
        </FadeIn>
      </main>
    </div>
  );
};

export default Dashboard;
