// frontend/src/App.jsx
import React, { useState } from "react";
import ProjectList from "./components/ProjectList";
import CertificationList from "./components/CertificationList";
import GithubStats from "./components/GithubStats";
import NostrProfile from "./components/NostrProfile";
import LatestNostrNote from "./components/LatestNostrNote";
import BitcoinTip from "./components/BitcoinTip";
import SkillMatcher from "./components/SkillMatcher";
import GithubContributions from "./components/GithubContributions";
import FadeIn from "./components/FadeIn";

function App() {
  const [highlightedProjects, setHighlightedProjects] = useState(null);
  // We no longer need searchedQuery state here.

  return (
    <div className="container mx-auto p-4 md:p-8 max-w-4xl">
      {/* Header fades in first */}
      <FadeIn>
        <header className="text-center mb-12">
          <NostrProfile />
          <div className="flex justify-center items-stretch space-x-4 mt-6">
            <GithubStats />
            <BitcoinTip />
          </div>
        </header>
      </FadeIn>

      {/* Each main section fades in sequentially */}
      <FadeIn delay={200}>
        <LatestNostrNote />
      </FadeIn>

      <main>
        <FadeIn delay={300}>
          <SkillMatcher setHighlightedProjects={setHighlightedProjects} />
        </FadeIn>

        <FadeIn delay={400}>
          <GithubContributions />
        </FadeIn>

        <FadeIn delay={500}>
          <ProjectList highlightedProjects={highlightedProjects} />
        </FadeIn>

        <FadeIn delay={600}>
          <CertificationList />
        </FadeIn>
      </main>

      <FadeIn delay={700}>
        <footer className="text-center mt-12 py-6 text-gray-500 border-t border-gray-800">
          <p>Built with Django, React, Nostr, and ₿</p>
          <p>© {new Date().getFullYear()} Maximoto. All Rights Reserved.</p>
        </footer>
      </FadeIn>
    </div>
  );
}

export default App;
