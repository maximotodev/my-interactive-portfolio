// frontend/src/components/ChatAssistant.jsx

import React, { useState, useRef, useEffect } from "react";
import { postChatMessage } from "../api";
import { Link } from "react-router-dom";
import {
  FaPaperPlane,
  FaSpinner,
  FaCommentDots,
  FaTimes,
  FaLink,
} from "react-icons/fa";
import ReactMarkdown from "react-markdown";

// Sub-component for a single source link
const SourceLink = ({ source }) => {
  if (!source || !source.url) return null;
  const linkText = `${source.title} (${source.type})`;
  if (source.url.startsWith("/")) {
    return (
      <Link
        to={source.url}
        className="flex items-center gap-2 text-sm font-semibold text-purple-600 dark:text-purple-400 hover:underline"
      >
        <FaLink size={12} />
        <span>{linkText}</span>
      </Link>
    );
  }
  return (
    <a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-2 text-sm font-semibold text-purple-600 dark:text-purple-400 hover:underline"
    >
      <FaLink size={12} />
      <span>{linkText}</span>
    </a>
  );
};

// Sub-component to render the list of source links
const SourceList = ({ sources }) => {
  if (!sources || sources.length === 0) return null;
  return (
    <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
      <h4 className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-2">
        Relevant Links:
      </h4>
      <div className="space-y-1">
        {sources.map((source) => (
          <SourceLink key={source.url} source={source} />
        ))}
      </div>
    </div>
  );
};

const ChatAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm a factual AI assistant. Ask me anything about Maximoto's portfolio.",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () =>
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: "user", content: input.trim(), sources: [] };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const { data } = await postChatMessage(userMessage.content);
      const assistantMessage = {
        role: "assistant",
        content: data.answer,
        sources: data.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat API error:", error);
      const errorMessage = {
        role: "assistant",
        content: "Sorry, I'm having trouble connecting right now.",
        sources: [],
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 left-4 bg-purple-600 text-white p-4 rounded-full shadow-lg transform hover:scale-110 z-50"
      >
        {isOpen ? <FaTimes size={20} /> : <FaCommentDots size={20} />}
      </button>

      {isOpen && (
        <div className="fixed bottom-20 left-4 w-full max-w-md h-[70vh] bg-white dark:bg-gray-800 shadow-2xl rounded-lg flex flex-col z-50 ring-1 ring-black/10 dark:ring-white/10">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
              Factual AI Assistant
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Provides direct answers and sources.
            </p>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-lg flex flex-col ${
                    msg.role === "user"
                      ? "bg-purple-600 text-white"
                      : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                  }`}
                >
                  <ReactMarkdown
                    components={{
                      p: ({ node, ...props }) => (
                        <p className="mb-2 last:mb-0" {...props} />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul
                          className="list-disc list-inside space-y-1"
                          {...props}
                        />
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                  <SourceList sources={msg.sources} />
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="p-3 rounded-lg bg-gray-200 dark:bg-gray-700">
                  <FaSpinner className="animate-spin text-gray-500" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form
            onSubmit={handleSend}
            className="p-4 border-t border-gray-200 dark:border-gray-700 flex items-center"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 p-2 rounded-md bg-gray-100 dark:bg-gray-600 border-gray-300 dark:border-gray-500 focus:ring-2 focus:ring-purple-500 outline-none"
              placeholder="Ask a direct question..."
              disabled={isLoading}
            />
            <button
              type="submit"
              className="ml-2 p-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:bg-gray-500"
              disabled={isLoading}
            >
              <FaPaperPlane />
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatAssistant;
