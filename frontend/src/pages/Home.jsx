// frontend/src/pages/Home.jsx
import React, { useState } from "react";

// Import the custom hook we created.
import { useDebounce } from "../hooks/useDebounce";

// Import all the components this page will render.
import NostrProfile from "../components/NostrProfile";
import GithubStats from "../components/GithubStats";
import BitcoinTip from "../components/BitcoinTip";
import LatestNostrNote from "../components/LatestNostrNote";
import SkillMatcher from "../components/SkillMatcher";
import GithubContributions from "../components/GithubContributions";
import ProjectList from "../components/ProjectList";
import CertificationList from "../components/CertificationList";
import FadeIn from "../components/FadeIn";

const Home = () => {
  // This state holds the user's LIVE input from the search box.
  const [searchQuery, setSearchQuery] = useState("");

  // This is our debounced value. It will only update to match searchQuery
  // after the user has stopped typing for 300 milliseconds.
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

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

      {/* --- THIS IS THE CORRECTED MAIN SECTION --- */}
      <main>
        {/* GithubContributions appears first, with the first delay */}
        <FadeIn delay={300}>
          <GithubContributions />
        </FadeIn>

        {/* SkillMatcher appears second, with the next delay */}
        <FadeIn delay={400}>
          <SkillMatcher
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
          />
        </FadeIn>

        {/* ProjectList appears third, right below the matcher */}
        <FadeIn delay={500}>
          <ProjectList searchQuery={debouncedSearchQuery} />
        </FadeIn>

        {/* Certifications appear last */}
        <FadeIn delay={600}>
          <CertificationList />
        </FadeIn>
      </main>
    </>
  );
};

export default Home;
