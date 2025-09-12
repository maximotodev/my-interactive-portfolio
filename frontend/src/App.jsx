import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ThemeToggle from "./components/ThemeToggle";
import ChatAssistant from "./components/ChatAssistant";
import NostrLogin from "./components/NostrLogin";
import { useNostr } from "./context/NostrContext";
const CreateListing = lazy(() => import("./pages/CreateListing"));
// Correctly lazy load pages
const Home = lazy(() => import("./pages/Home"));
const BlogList = lazy(() => import("./pages/BlogList"));
const BlogPost = lazy(() => import("./pages/BlogPost"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Marketplace = lazy(() => import("./pages/Marketplace"));

const PageLoader = () => (
  <div className="flex justify-center items-center h-64">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 dark:border-purple-500"></div>
  </div>
);

function App() {
  const { isLoggedIn } = useNostr();
  return (
    <Router>
      <div className="container mx-auto p-4 md:p-8 max-w-5xl">
        <nav className="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-8 mb-12 text-lg">
          <Link
            to="/"
            className="text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-medium"
          >
            Home
          </Link>
          <Link
            to="/blog"
            className="text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-medium"
          >
            Blog
          </Link>
          <Link
            to="/dashboard"
            className="text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-medium"
          >
            Dashboard
          </Link>
          <Link
            to="/market"
            className="text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 font-medium"
          >
            Marketplace
          </Link>
          <NostrLogin />
        </nav>

        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/blog" element={<BlogList />} />
            <Route path="/blog/:slug" element={<BlogPost />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/market" element={<Marketplace />} />
            <Route path="/market/new" element={<CreateListing />} />
          </Routes>
        </Suspense>
        {/* Conditionally show a "Create Listing" button */}
        {isLoggedIn && (
          <Link
            to="/market/new"
            className="fixed bottom-20 right-4 bg-purple-600 text-white p-4 rounded-full shadow-lg"
          >
            + New Listing
          </Link>
        )}
        <ThemeToggle />
        <ChatAssistant />

        <footer className="text-center mt-12 py-6 text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-800">
          <p>Built with Django, React, Nostr, and ₿</p>
          <p>© {new Date().getFullYear()} Maximoto. All Rights Reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
