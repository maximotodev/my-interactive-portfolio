import React, { useState, useEffect } from "react";
import { FaServer, FaReact, FaPython } from "react-icons/fa";
import { SiDjango } from "react-icons/si";

const LoadingOverlay = ({ isVisible }) => {
  const [messageIndex, setMessageIndex] = useState(0);

  const messages = [
    "Connecting to the server...",
    "Waking up the free-tier instance...",
    "This can take a moment...",
    "This portfolio is built with:",
    "Python, Django, and PostgreSQL on the backend...",
    "React and TailwindCSS on the frontend...",
    "And is deployed on Render and Vercel...",
    "Almost there...",
  ];

  useEffect(() => {
    if (isVisible) {
      const interval = setInterval(() => {
        setMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
      }, 2500); // Change message every 2.5 seconds

      return () => clearInterval(interval);
    }
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-gray-100 dark:bg-gray-900 z-50 flex flex-col items-center justify-center transition-opacity duration-500">
      <div className="text-center">
        <div className="relative flex justify-center items-center mb-6">
          <FaServer className="text-5xl text-purple-500 animate-pulse" />
          <div className="absolute flex justify-center items-center">
            <span className="animate-ping absolute inline-flex h-16 w-16 rounded-full bg-purple-400 opacity-75"></span>
          </div>
        </div>
        <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">
          Welcome to My Interactive Portfolio
        </h1>
        <p className="text-gray-600 dark:text-gray-400 transition-opacity duration-500">
          {messages[messageIndex]}
        </p>
        <div className="flex justify-center space-x-4 mt-6 text-3xl text-gray-400 dark:text-gray-500">
          <FaPython />
          <SiDjango />
          <FaReact />
        </div>
      </div>
    </div>
  );
};

export default LoadingOverlay;
