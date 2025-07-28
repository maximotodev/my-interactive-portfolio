// frontend/src/components/ChatAssistant.jsx
import React, { useState, useRef, useEffect } from "react";
import { postChatMessage } from "../api";
import {
  FaPaperPlane,
  FaSpinner,
  FaCommentDots,
  FaTimes,
} from "react-icons/fa";
import ReactMarkdown from "react-markdown";

const ChatAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm Maximoto's AI assistant. Feel free to ask me anything about his projects or skills.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const { data } = await postChatMessage(input);
      const assistantMessage = { role: "assistant", content: data.answer };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat API error:", error);
      const errorMessage = {
        role: "assistant",
        content:
          "Sorry, I'm having trouble connecting. Please try again later.",
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
        className="fixed bottom-4 left-4 bg-purple-600 text-white p-4 rounded-full shadow-lg transform hover:scale-110 transition-transform z-50"
        aria-label="Toggle Chat Assistant"
      >
        {isOpen ? <FaTimes size={20} /> : <FaCommentDots size={20} />}
      </button>

      {isOpen && (
        <div className="fixed bottom-20 left-4 w-full max-w-md h-[70vh] bg-white dark:bg-gray-800 shadow-2xl rounded-lg flex flex-col z-50 ring-1 ring-black/10 dark:ring-white/10">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
              AI Career Assistant
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Ask about my experience and certifications
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
                  className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-purple-600 text-white"
                      : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                  }`}
                >
                  {/* --- THIS IS THE FIX --- */}
                  <ReactMarkdown
                    // The 'className' prop is removed.
                    // We use the 'components' prop to apply Tailwind styles to the HTML elements
                    // that react-markdown generates.
                    components={{
                      p: ({ node, ...props }) => (
                        <p className="mb-2 last:mb-0" {...props} />
                      ),
                      ol: ({ node, ...props }) => (
                        <ol className="list-decimal list-inside" {...props} />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul className="list-disc list-inside" {...props} />
                      ),
                      a: ({ node, ...props }) => (
                        <a
                          className="text-purple-400 hover:underline"
                          {...props}
                        />
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
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
              className="flex-1 p-2 rounded-md bg-gray-100 dark:bg-gray-600 text-gray-900 dark:text-white border-gray-300 dark:border-gray-500 focus:ring-2 focus:ring-purple-500 outline-none"
              placeholder="e.g., What is Tribev2?"
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
