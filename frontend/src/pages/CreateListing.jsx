// frontend/src/pages/CreateListing.jsx
import React, { useState } from "react";
import { useNostr } from "../context/NostrContext";
import { useNavigate } from "react-router-dom";

const CreateListing = () => {
  const { isLoggedIn, pubkey } = useNostr();
  const navigate = useNavigate();
  const [listing, setListing] = useState({
    name: "",
    description: "",
    price: "",
    image: "",
  });
  const [status, setStatus] = useState("idle"); // idle, publishing, success, error

  if (!isLoggedIn) {
    return (
      <div className="text-center p-8">
        <h2 className="text-2xl font-bold">Access Denied</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Please log in with your Nostr extension to create a listing.
        </p>
      </div>
    );
  }

  const handleChange = (e) =>
    setListing((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("publishing");
    try {
      const newEvent = {
        kind: 30402,
        pubkey: pubkey,
        created_at: Math.floor(Date.now() / 1000),
        tags: [],
        content: JSON.stringify({
          name: listing.name,
          description: listing.description,
          price: listing.price, // Keep as string for now, backend will handle int conversion
          image: listing.image,
        }),
      };

      const signedEvent = await window.nostr.signEvent(newEvent);

      // For now, we just log the signed event. In a real app, you'd publish this.
      console.log("Signed Marketplace Listing Event:", signedEvent);

      setStatus("success");
      setTimeout(() => navigate("/market"), 2000); // Redirect after success
    } catch (error) {
      console.error("Failed to sign or publish event:", error);
      setStatus("error");
    }
  };

  // ... (Return a form similar to the ContactForm, with fields for name, description, price, image)
  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-8">
        Create New Marketplace Listing
      </h1>
      {/* ... Form JSX here ... */}
      <form onSubmit={handleSubmit}>
        {/* ... input fields for name, description, price, image ... */}
        <button type="submit" disabled={status === "publishing"}>
          {status === "publishing"
            ? "Publishing..."
            : "Publish Listing to Nostr"}
        </button>
        {status === "success" && (
          <p className="text-green-500">Success! Redirecting...</p>
        )}
        {status === "error" && (
          <p className="text-red-500">Failed to publish listing.</p>
        )}
      </form>
    </div>
  );
};

export default CreateListing;
