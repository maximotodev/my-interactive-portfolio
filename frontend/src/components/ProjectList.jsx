// frontend/src/components/ProjectList.jsx
import React, { useState, useEffect } from "react";
import { fetchProjects } from "../api";
import ProjectListSkeleton from "./ProjectListSkeleton";

const ProjectList = ({ highlightedProjects }) => {
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
  }, []);

  if (isLoading) return <ProjectListSkeleton />;

  // --- FINAL, CORRECT LOGIC ---

  // A search is active if `highlightedProjects` is an array (even an empty one).
  // It is inactive if it's null.
  const isSearchActive = highlightedProjects !== null;

  let projectsToShow = [];
  if (isSearchActive) {
    const highlightedIds = new Set(highlightedProjects.map((p) => p.id));
    projectsToShow = allProjects.filter((p) => highlightedIds.has(p.id));
  } else {
    // If no search is active, show all projects.
    projectsToShow = allProjects;
  }

  return (
    <section className="my-12">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold mb-2">My Projects</h2>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto">
          {!isSearchActive
            ? "The recent projects are listed below."
            : `Showing ${projectsToShow.length} matched project(s).`}{" "}
          Others can be found on my{" "}
          <a
            href="https://github.com/maximotodev"
            target="_blank"
            rel="noopener noreferrer"
            className="text-purple-400 hover:underline font-semibold"
          >
            GitHub
          </a>
          .
        </p>
      </div>

      {/* Conditional rendering for no results */}
      {isSearchActive && projectsToShow.length === 0 && (
        <div className="text-center p-8 bg-gray-800 rounded-lg mt-4">
          <p className="text-xl text-gray-300">No projects match your query.</p>
          <p className="text-gray-400">
            Try broadening your search terms or clear the search to see all
            projects.
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-4">
        {projectsToShow.map((project) => (
          <div
            key={project.id}
            className="bg-gray-800 rounded-lg shadow-xl overflow-hidden ring-1 ring-white/10 transition-all duration-300 ease-in-out transform hover:-translate-y-1"
          >
            {project.image && (
              <img
                src={project.image}
                alt={project.title}
                className="w-full h-48 object-cover"
              />
            )}
            <div className="p-6">
              <h3 className="text-xl font-bold text-purple-400">
                {project.title}
              </h3>
              <p className="text-gray-300 mt-2 h-24 overflow-y-auto">
                {project.description}
              </p>
              <p className="text-sm text-gray-400 mt-4">
                <b>Technologies:</b> {project.technologies}
              </p>
              <div className="mt-4 space-x-4">
                {project.repository_url && (
                  <a
                    href={project.repository_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-yellow-400 hover:text-yellow-300 transition-colors"
                  >
                    Repo
                  </a>
                )}
                {project.live_url && (
                  <a
                    href={project.live_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-yellow-400 hover:text-yellow-300 transition-colors"
                  >
                    Live Demo
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProjectList;
