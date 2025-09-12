// frontend/src/components/NostrLogin.jsx
import React from "react";
import { useNostr } from "../context/NostrContext";
import { FaSignInAlt, FaSignOutAlt } from "react-icons/fa";

const NostrLogin = () => {
  const { isLoggedIn, login, logout, pubkey } = useNostr();

  if (isLoggedIn) {
    return (
      <div className="flex items-center gap-2">
        <span className="text-sm font-mono text-gray-500 hidden sm:block">
          {pubkey.substring(0, 6)}...{pubkey.substring(pubkey.length - 4)}
        </span>
        <button
          onClick={logout}
          className="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700"
          title="Logout"
        >
          <FaSignOutAlt />
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={login}
      className="flex items-center gap-2 px-3 py-1 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-sm font-medium"
      title="Login with Nostr"
    >
      <FaSignInAlt />
      Login
    </button>
  );
};

export default NostrLogin;
