// frontend/src/components/NostrProfile.jsx
import React, { useState, useEffect } from "react";
import { fetchNostrProfile } from "../api";

const NostrProfile = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getProfile = async () => {
      try {
        const { data } = await fetchNostrProfile();
        setUser(data);
      } catch (err) {
        setError("Could not load Nostr profile.");
        console.error(err);
      }
    };
    getProfile();
  }, []);

  // While loading, show a simplified skeleton
  if (!user && !error) {
    return (
      <div className="animate-pulse">
        <div className="h-32 w-32 rounded-full bg-gray-700 mx-auto"></div>
        <div className="h-8 w-48 bg-gray-700 rounded-md mx-auto mt-4"></div>
        <div className="h-5 w-80 bg-gray-700 rounded-md mx-auto mt-2"></div>
      </div>
    );
  }

  if (error) return <p className="text-red-400">{error}</p>;

  // We get the npub from the profile data itself if available
  const npub = user.nip05.split("@")[0]; // A simple way to get it, adjust if needed

  return (
    <div className="flex flex-col items-center">
      <img
        src={user.picture}
        alt={user.display_name}
        className="w-32 h-32 rounded-full border-4 border-purple-500 shadow-lg"
      />
      <h1 className="text-3xl md:text-4xl font-bold mt-4">
        {user.display_name || user.name}
      </h1>
      <p className="text-base md:text-lg text-gray-300 max-w-xl mx-auto mt-2">
        {user.about}
      </p>

      {/* --- ADD THIS BUTTON --- */}
      {npub && (
        <a
          href={`https://primal.net/p/${npub}`}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 inline-block bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-100"
        >
          View on Nostr
        </a>
      )}
    </div>
  );
};

export default NostrProfile;
