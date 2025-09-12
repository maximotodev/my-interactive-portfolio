import React, { useState, useEffect } from "react";
import { fetchProjects } from "../api";
import FadeIn from "./FadeIn";
import ProjectListSkeleton from "./ProjectListSkeleton";

const ProjectList = ({ selectedTag, onTagSelect, onClearFilter }) => {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Using an AbortController for safe cleanup
    const abortController = new AbortController();

    const getProjects = async () => {
      setIsLoading(true);
      try {
        // Pass the tag's slug and the abort signal to the API call
        const { data } = await fetchProjects(selectedTag?.slug, {
          signal: abortController.signal,
        });

        // --- THIS IS THE DEFINITIVE FIX ---
        // We now correctly handle the paginated API response.
        if (data && Array.isArray(data.results)) {
          setProjects(data.results);
        } else if (Array.isArray(data)) {
          // Fallback for non-paginated responses
          setProjects(data);
        } else {
          console.error(
            "Unexpected API response structure for projects:",
            data
          );
          setProjects([]);
        }
      } catch (error) {
        if (error.name !== "CanceledError") {
          console.error("Failed to fetch projects:", error);
          setProjects([]);
        }
      } finally {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      }
    };
    getProjects();

    return () => {
      abortController.abort();
    };
  }, [selectedTag]); // Re-run whenever selectedTag changes

  if (isLoading) {
    return <ProjectListSkeleton />;
  }

  return (
    <section className="my-12">
      {selectedTag && (
        <div className="text-center mb-10 p-4 bg-purple-100 dark:bg-purple-900/50 rounded-lg">
          <p className="text-lg text-purple-800 dark:text-purple-200">
            Showing projects tagged with:{" "}
            <strong className="font-bold">{selectedTag.name}</strong>
          </p>
          <button
            onClick={onClearFilter}
            className="mt-2 text-sm font-semibold text-purple-600 dark:text-purple-300 hover:underline"
          >
            Clear Filter
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
        {projects.map((project, index) => (
          <FadeIn key={project.id} delay={index * 100}>
            <div className="group bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden ring-1 ring-black/5 dark:ring-white/10 transition-all duration-300 ease-in-out transform hover:-translate-y-1.5 hover:shadow-2xl hover:ring-purple-500">
              <img
                src={project.image}
                alt={project.title}
                className="w-full h-48 object-cover"
                loading="lazy"
              />
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                  {project.title}
                </h3>
                <p className="text-gray-700 dark:text-gray-300 mt-2 h-24 overflow-y-auto">
                  {project.description}
                </p>
                {project.tags && project.tags.length > 0 && (
                  <div className="mt-4">
                    <h4 className="text-sm font-bold text-gray-600 dark:text-gray-400 mb-2">
                      Technologies & Skills:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {project.tags.map((tag) => (
                        <button
                          key={tag.slug}
                          onClick={() => onTagSelect(tag)}
                          className="px-2.5 py-0.5 bg-gray-200 dark:bg-gray-700 text-xs font-semibold text-gray-700 dark:text-gray-200 rounded-full hover:bg-purple-200 dark:hover:bg-purple-700 hover:text-purple-800 dark:hover:text-white transition-colors"
                        >
                          {tag.name}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700 space-x-4">
                  <a
                    href={project.repository_url}
                    className="font-semibold text-yellow-600 dark:text-yellow-400 hover:underline"
                  >
                    Repo
                  </a>
                  <a
                    href={project.live_url}
                    className="font-semibold text-yellow-600 dark:text-yellow-400 hover:underline"
                  >
                    Live Demo
                  </a>
                </div>
              </div>
            </div>
          </FadeIn>
        ))}
      </div>

      {!isLoading && projects.length === 0 && (
        <div className="text-center p-8 bg-white dark:bg-gray-800 rounded-lg">
          <p className="text-xl text-gray-800 dark:text-gray-300">
            No projects found for this tag.
          </p>
          <p className="text-gray-600 dark:text-gray-400">
            Try selecting another tag or clearing the filter.
          </p>
        </div>
      )}
    </section>
  );
};

export default ProjectList;
