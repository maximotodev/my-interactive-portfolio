// frontend/src/components/FadeIn.jsx
import React from "react";
import { useInView } from "react-intersection-observer";

const FadeIn = ({ children, delay = 0, direction = "up" }) => {
  const { ref, inView } = useInView({
    triggerOnce: true, // Only animate once
    threshold: 0.1, // Trigger when 10% of the element is visible
  });

  const getDirectionClass = () => {
    switch (direction) {
      case "down":
        return "translate-y-[-20px]";
      case "left":
        return "translate-x-[-20px]";
      case "right":
        return "translate-x-[20px]";
      default:
        return "translate-y-[20px]"; // 'up' is the default
    }
  };

  return (
    <div
      ref={ref}
      className={`
        transition-all duration-700 ease-in-out
        ${
          inView
            ? "opacity-100 translate-y-0 translate-x-0"
            : `opacity-0 ${getDirectionClass()}`
        }
      `}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};

export default FadeIn;
