// frontend/src/components/PortfolioSearch.jsx

import React from "react";
import { FaSearch } from "react-icons/fa";

// This is a "controlled component" for the search input.
const PortfolioSearch = ({ searchQuery, setSearchQuery }) => {
  return (
    <div className="my-12 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl ring-1 ring-black/5 dark:ring-white/10">
      <h2 className="text-2xl font-bold mb-4 text-purple-600 dark:text-purple-400">
        Portfolio Full-Text Search
      </h2>
      <p className="mb-4 text-gray-600 dark:text-gray-300">
        Search across my projects and blog posts. Try "React", "AI", or
        "Bitcoin".
      </p>
      <div className="relative">
        <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          className="w-full p-3 pl-12 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white border border-transparent focus:outline-none focus:ring-2 focus:ring-purple-500 transition-shadow"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search for a technology or concept..."
        />
      </div>
    </div>
  );
};

export default PortfolioSearch;
