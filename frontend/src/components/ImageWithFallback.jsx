import React, { useState } from "react";
import { FaStore } from "react-icons/fa";

const ImageWithFallback = ({ src, alt, className }) => {
  const [hasError, setHasError] = useState(false);

  const handleError = () => {
    setHasError(true);
  };

  // If there's an error (e.g., image 404s or is broken),
  // or if the src is empty/null, render the placeholder.
  if (hasError || !src) {
    return (
      <div
        className={`${className} bg-gray-200 dark:bg-gray-700 flex items-center justify-center`}
      >
        <FaStore className="text-4xl text-gray-400 dark:text-gray-500" />
      </div>
    );
  }

  // Otherwise, render the actual image.
  return (
    <img src={src} alt={alt} className={className} onError={handleError} />
  );
};

export default ImageWithFallback;
