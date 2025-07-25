// frontend/src/components/ThemeToggle.jsx
import React from "react";
import { useTheme } from "../context/ThemeContext";
// Import some nice icons
import { FaSun, FaMoon, FaDesktop } from "react-icons/fa6";

const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();

  const themes = [
    { name: "light", icon: <FaSun /> },
    { name: "dark", icon: <FaMoon /> },
    { name: "system", icon: <FaDesktop /> },
  ];

  const cycleTheme = () => {
    const currentIndex = themes.findIndex((t) => t.name === theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    setTheme(themes[nextIndex].name);
  };

  const currentIcon = themes.find((t) => t.name === theme)?.icon;

  return (
    <button
      onClick={cycleTheme}
      className="fixed bottom-4 right-4 bg-gray-700 dark:bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 ring-offset-2 ring-offset-gray-900 transition-colors"
      aria-label="Toggle theme"
      title={`Current theme: ${theme}`}
    >
      {currentIcon}
    </button>
  );
};

export default ThemeToggle;
