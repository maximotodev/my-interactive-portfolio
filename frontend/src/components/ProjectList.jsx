// frontend/src/components/ProjectList.jsx
import React, { useState, useEffect, useMemo } from "react";
import { fetchProjects } from "../api";
import ProjectListSkeleton from "./ProjectListSkeleton";

// The component now accepts the live `searchQuery` from the user's input.
const ProjectList = ({ searchQuery }) => {
  // This state holds ALL projects and is our single source of truth.
  // It's fetched only once when the component mounts.
  const [allProjects, setAllProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getProjects = async () => {
      setIsLoading(true);
      try {
        const { data } = await fetchProjects();
        setAllProjects(data);
      } catch (error) {
        console.error("Failed to fetch projects:", error);
      } finally {
        setIsLoading(false);
      }
    };
    getProjects();
  }, []); // The empty dependency array [] ensures this runs only once.

  // --- NEW REAL-TIME FILTERING LOGIC ---
  // `useMemo` is a React hook for performance. It ensures this filtering logic
  // only re-runs when the `searchQuery` or `allProjects` list changes.
  const filteredProjects = useMemo(() => {
    // If the search box is empty, return all projects.
    if (!searchQuery.trim()) {
      return allProjects;
    }

    const lowercasedQuery = searchQuery.toLowerCase();

    // Filter the master list of projects.
    return allProjects.filter((project) => {
      // Create a single string of all searchable text for a project.
      const projectText = `
                ${project.title} 
                ${project.description} 
                ${project.technologies}
            `.toLowerCase();

      // Return true if the project's text includes the search query.
      return projectText.includes(lowercasedQuery);
    });
  }, [searchQuery, allProjects]); // Dependencies for the useMemo hook

  // Show a skeleton loader while the initial project list is being fetched.
  if (isLoading) {
    return <ProjectListSkeleton />;
  }

  const isSearchActive = searchQuery.trim() !== "";
  const introText = isSearchActive
    ? `Showing ${filteredProjects.length} project(s) matching "${searchQuery}"`
    : "The recent projects are listed below.";

  return (
    <section className="my-12">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold mb-2 text-gray-900 dark:text-gray-100">
          My Projects
        </h2>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          {introText} Others can be found on my{" "}
          <a
            href="https://github.com/maximotodev"
            target="_blank"
            rel="noopener noreferrer"
            className="text-purple-600 dark:text-purple-400 hover:underline font-semibold"
          >
            GitHub
          </a>
          .
        </p>
      </div>

      {/* If a search is active and finds no results, show this message */}
      {isSearchActive && filteredProjects.length === 0 && (
        <div className="text-center p-8 bg-white dark:bg-gray-800 rounded-lg">
          <p className="text-xl text-gray-800 dark:text-gray-300">
            No projects match your query.
          </p>
          <p className="text-gray-600 dark:text-gray-400">
            Try broadening your search terms or clear the search to see all
            projects.
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
        {allProjects.map((project) => (
          <div
            key={project.id}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden ring-1 ring-black/5 dark:ring-white/10 transition-all duration-300 ease-in-out transform hover:-translate-y-1"
          >
            {project.image && (
              <img
                src={project.image}
                alt={project.title}
                className="w-full h-48 object-cover"
                loading="lazy"
              />
            )}
            <div className="p-6">
              <h3 className="text-xl font-bold text-purple-600 dark:text-purple-400">
                {project.title}
              </h3>
              <p className="text-gray-700 dark:text-gray-300 mt-2 h-24 overflow-y-auto">
                {project.description}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-4">
                <b>Technologies:</b> {project.technologies}
              </p>
              <div className="mt-4 space-x-4">
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
        ))}
      </div>
    </section>
  );
};

export default ProjectList;
