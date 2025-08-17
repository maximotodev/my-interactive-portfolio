// frontend/src/pages/Home.jsx
import React, { useState } from "react";
import NostrProfile from "../components/NostrProfile";
import GithubStats from "../components/GithubStats";
import BitcoinTip from "../components/BitcoinTip";
import LatestNostrNote from "../components/LatestNostrNote";
import GithubContributions from "../components/GithubContributions";
import ProjectList from "../components/ProjectList";
import CertificationList from "../components/CertificationList";
import MempoolStats from "../components/MempoolStats";
import FadeIn from "../components/FadeIn";
import TagCloud from "../components/TagCloud"; // <-- 1. IMPORT TAG CLOUD

const Home = () => {
  // --- 2. LIFTED STATE: The Home page now controls the filter ---
  const [selectedTag, setSelectedTag] = useState(null);

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

        {/* --- 3. ADD THE TAG CLOUD COMPONENT --- */}
        <FadeIn delay={500}>
          <TagCloud selectedTag={selectedTag} onTagSelect={setSelectedTag} />
        </FadeIn>

        {/* --- 4. PASS STATE DOWN TO THE PROJECT LIST --- */}
        <FadeIn delay={600}>
          <ProjectList
            selectedTag={selectedTag}
            onTagSelect={setSelectedTag}
            onClearFilter={() => setSelectedTag(null)}
          />
        </FadeIn>

        <FadeIn delay={700}>
          <CertificationList />
        </FadeIn>
      </main>
    </>
  );
};

export default Home;
