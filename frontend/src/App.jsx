// frontend/src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import BlogList from "./pages/BlogList";
import BlogPost from "./pages/BlogPost";

function App() {
  return (
    <Router>
      <div className="container mx-auto p-4 md:p-8 max-w-4xl">
        <nav className="flex justify-center space-x-8 mb-12 text-lg">
          <Link
            to="/"
            className="text-gray-300 hover:text-purple-400 transition-colors"
          >
            Home
          </Link>
          <Link
            to="/blog"
            className="text-gray-300 hover:text-purple-400 transition-colors"
          >
            Blog
          </Link>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/blog" element={<BlogList />} />
          <Route path="/blog/:slug" element={<BlogPost />} />
        </Routes>

        <footer className="text-center mt-12 py-6 text-gray-500 border-t border-gray-800">
          <p>Built with Django, React, Nostr, and ₿</p>
          <p>© {new Date().getFullYear()} Maximoto. All Rights Reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
