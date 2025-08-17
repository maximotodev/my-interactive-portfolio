import React, { useState, useEffect } from "react";
import { fetchTags } from "../api";

const TagCloud = ({ selectedTag, onTagSelect }) => {
  const [tags, setTags] = useState([]);

  useEffect(() => {
    const getTags = async () => {
      try {
        const { data } = await fetchTags();
        setTags(data);
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
    };
    getTags();
  }, []);

  if (tags.length === 0) {
    return null; // Don't render anything if there are no tags
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
