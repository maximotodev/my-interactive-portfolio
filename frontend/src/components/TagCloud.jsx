import React, { useState, useEffect } from "react";
import { fetchTags } from "../api";

const TagCloud = ({ selectedTag, onTagSelect }) => {
  // Initialize state to null to handle the initial loading state correctly
  const [tags, setTags] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Using an AbortController for safe cleanup
    const abortController = new AbortController();

    const getTags = async () => {
      try {
        const { data } = await fetchTags({ signal: abortController.signal });

        // --- THIS IS THE DEFINITIVE FIX ---
        // We now correctly handle the paginated API response.
        if (data && Array.isArray(data.results)) {
          setTags(data.results);
        } else if (Array.isArray(data)) {
          // Fallback for if pagination is ever disabled again
          setTags(data);
        } else {
          console.error("Unexpected API response structure for tags:", data);
          setTags([]);
        }
      } catch (error) {
        if (error.name !== "CanceledError") {
          console.error("Failed to fetch tags:", error);
          setTags([]);
        }
      } finally {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    getTags();

    return () => {
      abortController.abort();
    };
  }, []);

  // Show a simple loading state
  if (isLoading) {
    return (
      <div className="my-12 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl animate-pulse">
        <div className="h-7 w-1/2 bg-gray-300 dark:bg-gray-700 rounded"></div>
      </div>
    );
  }

  // Don't render anything if there are no tags or if there was an error
  if (!tags || tags.length === 0) {
    return null;
  }

  return (
    <div className="my-12 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl ring-1 ring-black/5 dark:ring-white/10">
      <h2 className="text-2xl font-bold mb-4 text-purple-600 dark:text-purple-400">
        Filter Projects by Tag
      </h2>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <button
            key={tag.slug}
            onClick={() => onTagSelect(tag)}
            className={`px-3 py-1 text-sm font-medium rounded-full transition-colors ${
              selectedTag?.slug === tag.slug
                ? "bg-purple-600 text-white"
                : "bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-purple-200 dark:hover:bg-purple-700"
            }`}
          >
            {tag.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TagCloud;
