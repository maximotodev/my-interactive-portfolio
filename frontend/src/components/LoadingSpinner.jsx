// frontend/src/components/LoadingSpinner.jsx
import React from "react";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-4">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
  </div>
);

export default LoadingSpinner;
