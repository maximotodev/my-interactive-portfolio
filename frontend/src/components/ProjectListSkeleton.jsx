// frontend/src/components/ProjectListSkeleton.jsx
import React from "react";

const SkeletonCard = () => (
  <div className="bg-gray-800 rounded-lg shadow-md overflow-hidden animate-pulse">
    <div className="w-full h-48 bg-gray-700"></div>
    <div className="p-6">
      <div className="h-6 w-3/4 bg-gray-700 rounded mb-4"></div>
      <div className="h-4 w-full bg-gray-700 rounded mb-2"></div>
      <div className="h-4 w-5/6 bg-gray-700 rounded mb-2"></div>
      <div className="h-4 w-1/2 bg-gray-700 rounded"></div>
      <div className="h-4 w-full bg-gray-700 rounded mt-6"></div>
    </div>
  </div>
);

const ProjectListSkeleton = () => {
  return (
    <section className="my-8">
      <div className="h-8 w-1/3 bg-gray-700 rounded animate-pulse mb-6"></div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    </section>
  );
};

export default ProjectListSkeleton;
