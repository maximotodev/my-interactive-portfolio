// frontend/src/pages/BlogList.jsx
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchPosts } from "../api";
import FadeIn from "../components/FadeIn";

const BlogList = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getPosts = async () => {
      try {
        // Use the imported function directly
        const { data } = await fetchPosts();
        setPosts(data);
      } catch (error) {
        console.error("Failed to fetch posts:", error);
      } finally {
        setIsLoading(false);
      }
    };
    getPosts();
  }, []);

  if (isLoading) return <p>Loading articles...</p>;

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
              className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl dark:ring-1 dark:ring-white/10 dark:hover:bg-gray-700"
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
