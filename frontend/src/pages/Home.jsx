// frontend/src/pages/Home.jsx
import React, { useState } from "react";
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
  const [highlightedProjects, setHighlightedProjects] = useState(null);

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
    </>
  );
};

export default Home;
