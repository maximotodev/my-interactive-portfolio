// frontend/src/components/Modal.jsx
import React from "react";

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) {
    return null;
  }

  return (
    // Backdrop
    <div
      className="fixed inset-0 bg-black bg-opacity-70 z-50 flex justify-center items-center"
      onClick={onClose} // Close modal if backdrop is clicked
    >
      {/* Modal Content */}
      <div
        className="bg-gray-800 rounded-lg shadow-2xl p-6 w-full max-w-sm mx-4 text-center relative"
        onClick={(e) => e.stopPropagation()} // Prevent modal from closing when its content is clicked
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-400 hover:text-white text-2xl font-bold"
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
};

export default Modal;
