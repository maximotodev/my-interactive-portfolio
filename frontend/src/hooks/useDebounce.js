// frontend/src/hooks/useDebounce.js
import { useState, useEffect } from "react";

// This custom hook takes a value and a delay, and only returns the latest
// value after the user has stopped typing for the specified delay.
export function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup function to cancel the timeout if the value changes
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
