// frontend/src/components/LatestNostrNote.jsx
import React, { useState, useEffect } from "react";
import { fetchLatestNote } from "../api";

// Helper function to format the time since the note was posted
const formatTimeAgo = (timestamp) => {
  const now = new Date();
  const seconds = Math.floor((now - new Date(timestamp * 1000)) / 1000);

  let interval = seconds / 31536000;
  if (interval > 1) return Math.floor(interval) + " years ago";
  interval = seconds / 2592000;
  if (interval > 1) return Math.floor(interval) + " months ago";
  interval = seconds / 86400;
  if (interval > 1) return Math.floor(interval) + " days ago";
  interval = seconds / 3600;
  if (interval > 1) return Math.floor(interval) + " hours ago";
  interval = seconds / 60;
  if (interval > 1) return Math.floor(interval) + " minutes ago";
  return Math.floor(seconds) + " seconds ago";
};

const LatestNostrNoteSkeleton = () => (
  <div className="my-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md ring-1 ring-black/5 dark:ring-white/10 animate-pulse">
    <div className="h-4 w-1/4 bg-gray-300 dark:bg-gray-700 rounded mb-4"></div>
    <div className="h-5 w-full bg-gray-300 dark:bg-gray-700 rounded mb-2"></div>
    <div className="h-5 w-5/6 bg-gray-300 dark:bg-gray-700 rounded"></div>
    <div className="h-4 w-1/3 bg-gray-300 dark:bg-gray-700 rounded mt-4 ml-auto"></div>
  </div>
);

const LatestNostrNote = () => {
  const [note, setNote] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchLatestNote()
      .then((response) => setNote(response.data))
      .catch((error) => console.error("Could not fetch latest note:", error))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <LatestNostrNoteSkeleton />;
  }

  if (!note) {
    // Don't render anything if no note was found
    return null;
  }

  return (
    <div className="my-8">
      <h3 className="text-lg font-semibold text-gray-500 dark:text-gray-400 mb-2">
        Latest Note on Nostr:
      </h3>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 ring-1 ring-black/5 dark:ring-white/10">
        <blockquote className="border-l-4 border-purple-500 pl-4">
          <p className="text-lg italic text-gray-700 dark:text-gray-200">
            {note.content}
          </p>
        </blockquote>
        <p className="text-right text-sm text-gray-500 dark:text-gray-400 mt-4">
          — Posted {formatTimeAgo(note.created_at)}
        </p>
      </div>
    </div>
  );
};

export default LatestNostrNote;
