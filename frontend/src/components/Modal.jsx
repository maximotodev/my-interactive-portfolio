// frontend/src/components/Modal.jsx
import React from "react";

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) {
    return null;
  }

  return (
    // Backdrop: a semi-transparent black overlay, consistent for both themes
    <div
      className="fixed inset-0 bg-black bg-opacity-70 z-50 flex justify-center items-center backdrop-blur-sm"
      onClick={onClose} // Close modal if backdrop is clicked
    >
      {/* Modal Content */}
      <div
        className="rounded-lg shadow-2xl p-6 w-full max-w-sm mx-4 text-center relative
                   bg-white dark:bg-gray-800 
                   ring-1 ring-black/5 dark:ring-white/10"
        onClick={(e) => e.stopPropagation()} // Prevent modal from closing when its content is clicked
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 
                     dark:text-gray-400 dark:hover:text-white 
                     text-3xl font-light leading-none"
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
};

export default Modal;
