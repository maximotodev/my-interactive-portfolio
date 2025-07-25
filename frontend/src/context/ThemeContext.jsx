// frontend/src/context/ThemeContext.jsx
import React, { createContext, useState, useEffect, useContext } from "react";

// Create the context
const ThemeContext = createContext();

// Create a custom hook to use the context
export const useTheme = () => useContext(ThemeContext);

// Create the provider component that will wrap our app
export const ThemeProvider = ({ children }) => {
  // State to hold the current theme. We initialize it from localStorage or default to 'system'
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "system";
  });

  useEffect(() => {
    const root = window.document.documentElement;

    const applyTheme = (newTheme) => {
      const isSystemDark = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;

      // Remove previous theme class
      root.classList.remove("dark", "light");

      let currentTheme;
      if (newTheme === "system") {
        currentTheme = isSystemDark ? "dark" : "light";
      } else {
        currentTheme = newTheme;
      }

      root.classList.add(currentTheme);
    };

    // Apply the theme whenever the 'theme' state changes
    applyTheme(theme);

    // Save the user's preference to localStorage
    localStorage.setItem("theme", theme);
  }, [theme]);

  // Provide the theme state and a function to update it to all child components
  const value = { theme, setTheme };

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
};
