// frontend/src/pages/Home.jsx
import React, { useState, useEffect } from "react";
// We will use one of your fastest API calls as a "ping" to wake the server.
import { fetchGithubStats } from "../api";
import { useDebounce } from "../hooks/useDebounce";
import { performSearch } from "../api";
import ContactForm from "../components/ContactForm";
import NostrProfile from "../components/NostrProfile";
import GithubStats from "../components/GithubStats";
import BitcoinTip from "../components/BitcoinTip";
import LatestNostrNote from "../components/LatestNostrNote";
import GithubContributions from "../components/GithubContributions";
import ProjectList from "../components/ProjectList";
import CertificationList from "../components/CertificationList";
import MempoolStats from "../components/MempoolStats";
import PortfolioSearch from "../components/PortfolioSearch";
import SearchResults from "../components/SearchResults";
import FadeIn from "../components/FadeIn";
import TagCloud from "../components/TagCloud";
import LoadingOverlay from "../components/LoadingOverlay";
const Home = () => {
  // This state machine manages the entire loading experience
  const [serverState, setServerState] = useState("warming_up"); // Start in the "warming up" state
  // --- NEW: State for the full-text search ---
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState({
    projects: [],
    posts: [],
  });
  const [isSearching, setIsSearching] = useState(false);
  // This effect runs only once on initial page load
  useEffect(() => {
    const wakeUpServer = async () => {
      try {
        // We ping the server with a lightweight request. We don't care about the
        // data yet, we just want to wake it up. This will take 0-50 seconds.
        await fetchGithubStats();
        // Once this request succeeds, the server is awake.
        setServerState("ready");
      } catch (error) {
        console.error("Server failed to wake up:", error);
        setServerState("error"); // We can handle this state too if we want
      }
    };

    wakeUpServer();
  }, []); // The empty dependency array ensures this runs only once
  const isServerReady = serverState === "ready";

  // Debounce the search query to prevent API calls on every keystroke
  const debouncedSearchQuery = useDebounce(searchQuery, 300);
  // State for tag filtering
  const [selectedTag, setSelectedTag] = useState(null);

  // Effect for full-text search
  useEffect(() => {
    // We don't want to run a text search if a tag is selected
    if (debouncedSearchQuery && !selectedTag) {
      setIsSearching(true);
      performSearch(debouncedSearchQuery)
        .then((response) => setSearchResults(response.data))
        .catch((error) => console.error("Search failed:", error))
        .finally(() => setIsSearching(false));
    } else {
      setSearchResults({ projects: [], posts: [] });
    }
  }, [debouncedSearchQuery, selectedTag]);
  // Handler to clear all filters
  const clearAllFilters = () => {
    setSearchQuery("");
    setSelectedTag(null);
  };

  const isSearchActive = debouncedSearchQuery.length > 0;
  return (
    <>
      {/* --- Phase 1 & 2: The Welcome/Loading Overlay --- */}
      {/* This is visible while the server is warming up. It receives `true` then fades out when server is ready. */}
      <LoadingOverlay isVisible={!isServerReady} />

      {/* --- Phase 3: The Grand Reveal --- */}
      {/* The main content is only mounted AFTER the server is ready. */}
      {isServerReady && (
        <>
          <FadeIn>
            <header className="text-center mb-12">
              <NostrProfile />
              <div className="flex justify-center items-stretch space-x-4 mt-6">
                <GithubStats />
                <BitcoinTip />
              </div>
            </header>
          </FadeIn>

          <FadeIn delay={200}>
            <LatestNostrNote />
          </FadeIn>
          <FadeIn delay={300}>
            <MempoolStats />
          </FadeIn>

          <main>
            <FadeIn delay={400}>
              <GithubContributions />
            </FadeIn>

            {/* --- We will now show BOTH search and tags --- */}
            <FadeIn delay={500}>
              <PortfolioSearch
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
              />
            </FadeIn>

            <FadeIn delay={600}>
              <TagCloud
                selectedTag={selectedTag}
                onTagSelect={setSelectedTag}
              />
            </FadeIn>

            {/* --- THIS IS THE FIX --- */}
            {/* The rendering logic is now cleaner and always passes the correct props. */}
            <FadeIn delay={100}>
              {isSearchActive ? (
                <SearchResults
                  results={searchResults}
                  isLoading={isSearching}
                  query={debouncedSearchQuery}
                />
              ) : (
                // Always pass the required props to ProjectList
                <ProjectList
                  selectedTag={selectedTag}
                  onTagSelect={setSelectedTag}
                  onClearFilter={clearAllFilters}
                />
              )}
            </FadeIn>

            <FadeIn delay={700}>
              <CertificationList />
            </FadeIn>
            <FadeIn delay={800}>
              <ContactForm />
            </FadeIn>
          </main>
        </>
      )}
    </>
  );
};

export default Home;
