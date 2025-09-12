// frontend/src/context/NostrContext.jsx
import React, { createContext, useState, useContext } from "react";

const NostrContext = createContext();

export const useNostr = () => useContext(NostrContext);

export const NostrProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [pubkey, setPubkey] = useState(null);
  const [npub, setNpub] = useState(null);

  const login = async () => {
    if (window.nostr) {
      try {
        const userPubkey = await window.nostr.getPublicKey();
        setPubkey(userPubkey);
        // A simple way to convert hex to npub on the frontend can be done,
        // but for now we'll just store the hex.
        setIsLoggedIn(true);
        console.log("Logged in with pubkey:", userPubkey);
        return true;
      } catch (error) {
        console.error("Nostr login failed:", error);
        return false;
      }
    } else {
      alert(
        "Nostr extension (like Alby) not found. Please install one to log in."
      );
      return false;
    }
  };

  const logout = () => {
    setIsLoggedIn(false);
    setPubkey(null);
    setNpub(null);
  };

  const value = { isLoggedIn, pubkey, npub, login, logout };

  return (
    <NostrContext.Provider value={value}>{children}</NostrContext.Provider>
  );
};
