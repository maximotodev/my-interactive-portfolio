// frontend/src/components/SkillMatcher.jsx
import React from "react";

// This is now a "controlled component" that just manages the input state.
const SkillMatcher = ({ searchQuery, setSearchQuery }) => {
  return (
    <div className="my-12 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl ring-1 ring-black/5 dark:ring-white/10">
      <h2 className="text-2xl font-bold mb-4 text-purple-600 dark:text-purple-400">
        Filter Projects by Skill
      </h2>
      <p className="mb-4 text-gray-600 dark:text-gray-300">
        Start typing a technology, keyword, or project title (e.g., "React",
        "Django", "Nostr") to instantly filter the list below.
      </p>
      <input
        type="text"
        className="w-full p-3 rounded bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-shadow"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="e.g., Python, JavaScript, API..."
      />
    </div>
  );
};

export default SkillMatcher;
