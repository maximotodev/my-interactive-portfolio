// frontend/src/pages/Home.jsx
import React, { useState, useEffect } from "react";
import { useDebounce } from "../hooks/useDebounce";
import { performSearch } from "../api";
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

const Home = () => {
  // --- NEW: State for the full-text search ---
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState({
    projects: [],
    posts: [],
  });
  const [isSearching, setIsSearching] = useState(false);

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
          <TagCloud selectedTag={selectedTag} onTagSelect={setSelectedTag} />
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
      </main>
    </>
  );
};

export default Home;
