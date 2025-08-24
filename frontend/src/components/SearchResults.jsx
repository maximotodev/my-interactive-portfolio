import React from "react";
import { Link } from "react-router-dom";
import { FaProjectDiagram, FaFileAlt } from "react-icons/fa";

const SearchResults = ({ results, isLoading, query }) => {
  if (!query) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="my-8 animate-pulse">
        <div className="h-6 w-1/3 bg-gray-300 dark:bg-gray-700 rounded mb-4"></div>
        <div className="space-y-4">
          <div className="h-20 bg-white dark:bg-gray-800 rounded-lg"></div>
          <div className="h-20 bg-white dark:bg-gray-800 rounded-lg"></div>
        </div>
      </div>
    );
  }

  const hasProjects = results.projects && results.projects.length > 0;
  const hasPosts = results.posts && results.posts.length > 0;

  if (!hasProjects && !hasPosts) {
    return (
      <div className="my-8 text-center p-8 bg-white dark:bg-gray-800 rounded-lg">
        <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200">
          No results found
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Try a different search term.
        </p>
      </div>
    );
  }

  return (
    <div className="my-8 space-y-8">
      {hasProjects && (
        <section>
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2 text-gray-800 dark:text-gray-200">
            <FaProjectDiagram /> Matching Projects
          </h3>
          <div className="space-y-4">
            {results.projects.map((project) => (
              // --- THE FIX: Add a 'project-' prefix to the key ---
              <a
                href={project.live_url}
                target="_blank"
                rel="noopener noreferrer"
                key={`project-${project.id}`}
                className="block p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl transition-shadow"
              >
                <h4 className="font-bold text-purple-600 dark:text-purple-400">
                  {project.title}
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                  {project.description}
                </p>
              </a>
            ))}
          </div>
        </section>
      )}

      {hasPosts && (
        <section>
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2 text-gray-800 dark:text-gray-200">
            <FaFileAlt /> Related Blog Posts
          </h3>
          <div className="space-y-4">
            {results.posts.map((post) => (
              // --- THE FIX: Add a 'post-' prefix to the key ---
              <Link
                to={`/blog/${post.slug}`}
                key={`post-${post.id}`}
                className="block p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl transition-shadow"
              >
                <h4 className="font-bold text-purple-600 dark:text-purple-400">
                  {post.title}
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Published on{" "}
                  {new Date(post.published_date).toLocaleDateString()}
                </p>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default SearchResults;
