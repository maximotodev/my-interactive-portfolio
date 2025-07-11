// frontend/src/components/SkillMatcher.jsx
import React, { useState } from "react";
import { matchSkills } from "../api";

const SkillMatcher = ({ setHighlightedProjects }) => {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleMatch = async (e) => {
    e.preventDefault();
    // If the query is empty, reset the highlighted projects to signal "show all"
    if (!query.trim()) {
      setHighlightedProjects(null); // Use null to signify "no active search"
      return;
    }
    setIsLoading(true);
    try {
      const { data: rankedProjects } = await matchSkills(query);
      setHighlightedProjects(rankedProjects);
    } catch (error) {
      console.error("Skill matching failed:", error);
      setHighlightedProjects([]); // Set to empty array on error
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="my-12 p-6 bg-gray-800 rounded-lg shadow-xl ring-1 ring-white/10">
      <h2 className="text-2xl font-bold mb-4 text-purple-400">
        AI Skill Matcher
      </h2>
      <p className="mb-4 text-gray-300">
        Paste a job description or list of required skills (e.g., "React, REST
        APIs, Python") to see my most relevant projects.
      </p>
      <form onSubmit={handleMatch}>
        <textarea
          className="w-full p-3 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-shadow"
          rows="3"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Looking for a developer with experience in Django and PostgreSQL..."
        />
        <button
          type="submit"
          disabled={isLoading}
          className="mt-4 px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg disabled:bg-gray-500 disabled:cursor-not-allowed transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-100"
        >
          {isLoading ? "Analyzing..." : "Find Relevant Projects"}
        </button>
      </form>
    </div>
  );
};

export default SkillMatcher;
