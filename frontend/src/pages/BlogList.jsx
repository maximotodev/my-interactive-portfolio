import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchPosts } from "../api";
import FadeIn from "../components/FadeIn";

const BlogList = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Using an AbortController for safe cleanup
    const abortController = new AbortController();

    const getPosts = async () => {
      try {
        const { data } = await fetchPosts({ signal: abortController.signal });

        // --- THIS IS THE DEFINITIVE FIX ---
        // We now correctly handle the paginated API response.
        if (data && Array.isArray(data.results)) {
          setPosts(data.results);
        } else if (Array.isArray(data)) {
          // Fallback for non-paginated responses
          setPosts(data);
        } else {
          console.error("Unexpected API response structure for posts:", data);
          setPosts([]);
        }
      } catch (error) {
        if (error.name !== "CanceledError") {
          console.error("Failed to fetch posts:", error);
          setPosts([]);
        }
      } finally {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      }
    };
    getPosts();

    return () => {
      abortController.abort();
    };
  }, []);

  if (isLoading) {
    return <p className="text-center mt-12">Loading articles...</p>;
  }

  return (
    <FadeIn>
      <div className="container mx-auto p-4 md:p-8 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8 text-purple-600 dark:text-purple-400 border-b-2 border-purple-500 pb-2">
          My Writings
        </h1>
        <div className="space-y-8">
          {posts.map((post) => (
            <Link
              to={`/blog/${post.slug}`}
              key={post.slug}
              className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl dark:ring-1 dark:ring-white/10 dark:hover:bg-gray-700 transition-all duration-300"
            >
              <h2 className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                {post.title}
              </h2>
              <p className="text-gray-500 dark:text-gray-400 mt-2">
                Published on{" "}
                {new Date(post.published_date).toLocaleDateString()}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </FadeIn>
  );
};

export default BlogList;
