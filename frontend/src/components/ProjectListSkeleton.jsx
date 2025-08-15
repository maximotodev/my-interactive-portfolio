import React from "react";

// This is a single, reusable skeleton card that mimics the project card's layout.
const SkeletonCard = () => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden animate-pulse">
    <div className="w-full h-48 bg-gray-200 dark:bg-gray-700"></div>
    <div className="p-6">
      <div className="h-6 w-3/4 bg-gray-300 dark:bg-gray-600 rounded mb-4"></div>
      <div className="h-4 w-full bg-gray-300 dark:bg-gray-600 rounded mb-2"></div>
      <div className="h-4 w-5/6 bg-gray-300 dark:bg-gray-600 rounded mb-4"></div>
      <div className="h-4 w-1/2 bg-gray-300 dark:bg-gray-600 rounded"></div>
      <div className="flex justify-between items-center mt-6">
        <div className="h-4 w-1/4 bg-gray-300 dark:bg-gray-600 rounded"></div>
        <div className="h-4 w-1/4 bg-gray-300 dark:bg-gray-600 rounded"></div>
      </div>
    </div>
  </div>
);

// This component renders a grid of the skeleton cards.
const ProjectListSkeleton = () => {
  return (
    <section className="my-12">
      <div className="h-8 w-1/3 bg-gray-300 dark:bg-gray-700 rounded animate-pulse mb-10 mx-auto"></div>
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
