// frontend/src/components/NostrProfile.jsx
import React, { useState, useEffect } from "react";
import { fetchNostrProfile } from "../api";
import LoadingSpinner from "./LoadingSpinner";

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

  if (error) return <p className="text-red-400">{error}</p>;
  if (!user)
    return (
      <div className="animate-pulse h-32 w-32 rounded-full bg-gray-700 mx-auto mb-4"></div>
    );

  return (
    <div className="flex flex-col items-center">
      <img
        src={user.picture}
        alt={user.display_name}
        className="w-32 h-32 rounded-full border-4 border-purple-500 shadow-lg"
      />
      <h1 className="text-4xl font-bold mt-4">
        {user.display_name || user.name}
      </h1>
      <p className="text-lg text-gray-300 max-w-xl mx-auto mt-2">
        {user.about}
      </p>
    </div>
  );
};

export default NostrProfile;
