// frontend/src/pages/BlogPost.jsx
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { fetchPostBySlug } from "../api";
import FadeIn from "../components/FadeIn";

const BlogPost = () => {
  const { slug } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const getPost = async () => {
      if (!slug) return;
      try {
        // Use the imported function directly
        const { data } = await fetchPostBySlug(slug);
        setPost(data);
      } catch (error) {
        console.error("Failed to fetch post:", error);
      }
    };
    getPost();
  }, [slug]);

  if (!post) return <p>Loading article...</p>;

  return (
    <FadeIn>
      <div className="container mx-auto p-4 md:p-8 max-w-3xl">
        <Link
          to="/blog"
          className="text-purple-600 dark:text-purple-400 hover:underline mb-8 block"
        >
          ← Back to all articles
        </Link>
        <article className="prose dark:prose-invert prose-lg lg:prose-xl max-w-none">
          <h1 className="text-yellow-600 dark:text-yellow-400">{post.title}</h1>
          <ReactMarkdown>{post.content}</ReactMarkdown>
        </article>
      </div>
    </FadeIn>
  );
};

export default BlogPost;
