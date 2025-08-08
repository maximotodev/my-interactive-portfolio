import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import {
  FaPaperPlane,
  FaCommentDots,
  FaTimes,
  FaUser,
  FaRobot,
  FaBriefcase,
  FaCode,
  FaCertificate,
  FaLink,
  FaGithub,
  FaRss,
  FaPython,
  FaReact,
  FaJs,
  FaDocker,
  FaDatabase,
  FaExclamationTriangle,
  FaInfoCircle,
} from "react-icons/fa";
import { SiVercel, SiTailwindcss, SiNextdotjs } from "react-icons/si";

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// --- FINAL, POLISHED GRAPHICAL COMPONENTS ---
const getTechIcon = (tech) => {
  const lowerTech = tech.toLowerCase();
  if (lowerTech.includes("react")) return <FaReact className="text-blue-400" />;
  if (lowerTech.includes("python"))
    return <FaPython className="text-yellow-400" />;
  if (lowerTech.includes("javascript"))
    return <FaJs className="text-yellow-300" />;
  if (lowerTech.includes("next.js"))
    return <SiNextdotjs className="dark:text-white text-black" />;
  if (lowerTech.includes("tailwind"))
    return <SiTailwindcss className="text-cyan-400" />;
  if (lowerTech.includes("vercel"))
    return <SiVercel className="dark:text-white text-black" />;
  if (lowerTech.includes("docker"))
    return <FaDocker className="text-blue-500" />;
  if (lowerTech.includes("sql") || lowerTech.includes("postgre"))
    return <FaDatabase className="text-blue-300" />;
  return <FaCode className="text-gray-400" />;
};
const TechStackCloud = ({ data }) => (
  <div className="my-2">
    <h3 className="flex items-center gap-2 font-bold text-lg mb-3 text-gray-800 dark:text-white">
      <FaCode /> Core Technology Stack
    </h3>
    <div className="flex flex-wrap gap-2">
      {data.technologies?.map((tech) => (
        <div
          key={tech}
          className="flex items-center gap-2 px-3 py-1 bg-gray-200 dark:bg-gray-600/80 text-gray-800 dark:text-gray-200 text-sm rounded-full font-medium"
        >
          {getTechIcon(tech)}
          <span>{tech}</span>
        </div>
      ))}
    </div>
  </div>
);
const ProjectCard = ({ data }) => (
  <div className="bg-white dark:bg-gray-700/50 rounded-lg p-4 my-2 ring-1 ring-gray-200 dark:ring-gray-900/50 shadow-md hover:shadow-purple-500/10 transition-shadow">
    <div className="flex items-center gap-3 mb-2">
      <h4 className="font-bold text-gray-800 dark:text-white">{data.title}</h4>
    </div>
    <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
      {data.description}
    </p>
    <div className="flex flex-wrap gap-2 mb-3">
      {data.technologies?.map((tech) => (
        <span
          key={tech}
          className="px-2 py-0.5 bg-purple-100 text-purple-800 dark:bg-purple-900/70 dark:text-purple-300 text-xs rounded-full font-medium"
        >
          {tech}
        </span>
      ))}
    </div>
    <div className="flex items-center gap-4 text-sm mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
      <a
        href={data.url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center gap-1.5 text-gray-600 dark:text-gray-300 hover:text-purple-500 transition-colors"
      >
        <FaLink /> Live Demo
      </a>
      <a
        href={data.repo_url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center gap-1.5 text-gray-600 dark:text-gray-300 hover:text-purple-500 transition-colors"
      >
        <FaGithub /> Repository
      </a>
    </div>
  </div>
);
const ExperienceTimeline = ({ items }) => (
  <div className="my-2">
    <h3 className="flex items-center gap-2 font-bold text-lg mb-3 text-gray-800 dark:text-white">
      <FaBriefcase className="text-gray-500" /> Professional Experience
    </h3>
    <div className="relative border-l-2 border-purple-200 dark:border-purple-800/50 ml-2">
      {items.map((item, index) => (
        <ExperienceTimelineItem
          key={index}
          data={item}
          isLast={index === items.length - 1}
        />
      ))}
    </div>
  </div>
);
const ExperienceTimelineItem = ({ data, isLast }) => (
  <div className={`relative pl-8 pb-6 ${isLast ? "pb-2" : ""}`}>
    <div className="absolute -left-[9px] top-1 w-4 h-4 bg-purple-500 rounded-full border-4 border-white dark:border-gray-700/80"></div>
    <p className="font-bold text-gray-800 dark:text-white">{data.title}</p>
    <p className="text-sm text-gray-600 dark:text-gray-400 font-medium">
      {data.company} • {data.date}
    </p>
    <ul className="list-disc pl-5 mt-2 text-sm text-gray-600 dark:text-gray-300 space-y-1">
      {data.responsibilities?.map((resp) => (
        <li key={resp}>{resp}</li>
      ))}
    </ul>
  </div>
);
const CertificationCard = ({ data }) => (
  <a
    href={data.url}
    target="_blank"
    rel="noopener noreferrer"
    className="flex items-center gap-4 p-3 my-2 bg-white dark:bg-gray-700/50 rounded-lg ring-1 ring-gray-200 dark:ring-gray-900/50 hover:ring-purple-500 transition-all shadow-md hover:shadow-lg"
  >
    <FaCertificate className="text-yellow-500 flex-shrink-0" size={24} />
    <div>
      <p className="font-bold text-gray-800 dark:text-white">{data.name}</p>
      <p className="text-sm text-gray-600 dark:text-gray-400">{data.issuer}</p>
    </div>
  </a>
);
const BlogCard = ({ data }) => (
  <a
    href={data.url}
    target="_blank"
    rel="noopener noreferrer"
    className="block p-4 my-2 bg-white dark:bg-gray-700/50 rounded-lg ring-1 ring-gray-200 dark:ring-gray-900/50 hover:ring-purple-500 transition-all shadow-md hover:shadow-lg"
  >
    <div className="flex items-center gap-3 mb-2">
      <FaRss className="text-blue-500 flex-shrink-0" />
      <h4 className="font-bold text-gray-800 dark:text-white">{data.title}</h4>
    </div>
    <p className="text-sm text-gray-600 dark:text-gray-300">{data.excerpt}</p>
  </a>
);
// --- NEW Graceful Failure Components ---
const EmptyStateCard = ({ query }) => (
  <div className="flex flex-col items-center gap-2 text-center p-4 bg-gray-100 dark:bg-gray-700/30 rounded-lg">
    <FaInfoCircle className="text-blue-400" size={20} />
    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
      No specific items found.
    </p>
    <p className="text-xs text-gray-500 dark:text-gray-400">
      My knowledge base didn't contain a direct match for that query.
    </p>
  </div>
);
const ErrorCard = ({ message }) => (
  <div className="flex flex-col items-center gap-2 text-center p-4 bg-red-100 dark:bg-red-900/30 rounded-lg">
    <FaExclamationTriangle className="text-red-500" size={20} />
    <p className="text-sm font-medium text-red-700 dark:text-red-300">
      An Error Occurred
    </p>
    <p className="text-xs text-red-600 dark:text-red-400">
      {message || "The AI model could not be reached."}
    </p>
  </div>
);

const ChatAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const suggestedPrompts = [
    "Show me projects",
    "Summarize experience",
    "What's your tech stack?",
    "Read the blog",
  ];

  useEffect(() => {
    if (isOpen && messages.length === 0)
      setMessages([
        {
          role: "assistant",
          content:
            "Hello! I'm Maxi. I can show you projects, experience, certifications, and more.",
        },
      ]);
  }, [isOpen]);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const handleSend = async (messageText) => {
    const text = messageText.trim();
    if (!text || isLoading) return;
    setMessages((prev) => [
      ...prev,
      { role: "user", content: text },
      { role: "assistant", content: null },
    ]);
    if (input) setInput("");
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });
      if (!response.ok) throw new Error("Request failed");
      const fullResponse = await response.text();

      // --- NEW: Bulletproof JSON Extractor ---
      // This looks for JSON that might be surrounded by other text.
      const jsonMatch = fullResponse.match(/(\[.*\]|\{.*\})/s);
      let finalContent;

      if (jsonMatch) {
        try {
          finalContent = JSON.parse(jsonMatch[0]);
        } catch (e) {
          // It looked like JSON but wasn't. Treat as text.
          finalContent = fullResponse;
        }
      } else {
        finalContent = fullResponse;
      }

      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1].content = finalContent;
        return newMessages;
      });
    } catch (error) {
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1].content = {
          error: "Sorry, I'm having trouble connecting.",
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleSend(input);
  };

  // --- FINAL "SMART RENDERER" ---
  const renderMessageContent = (content) => {
    if (content === null)
      return (
        <div className="flex items-center justify-center gap-1.5 p-2">
          <span className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></span>
          <span className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-75"></span>
          <span className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
        </div>
      );
    if (typeof content === "object" && content !== null) {
      if (content.error) return <ErrorCard message={content.error} />;
      if (Array.isArray(content) && content.length === 0)
        return <EmptyStateCard />;
      if (Array.isArray(content)) {
        const itemsByType = content.reduce((acc, item) => {
          acc[item.type] = acc[item.type] || [];
          acc[item.type].push(item);
          return acc;
        }, {});
        return (
          <div className="space-y-4">
            {itemsByType.project &&
              itemsByType.project.map((item, index) => (
                <ProjectCard key={index} data={item} />
              ))}
            {itemsByType.certification &&
              itemsByType.certification.map((item, index) => (
                <CertificationCard key={index} data={item} />
              ))}
            {itemsByType.experience && (
              <ExperienceTimeline items={itemsByType.experience} />
            )}
            {itemsByType.blog &&
              itemsByType.blog.map((item, index) => (
                <BlogCard key={index} data={item} />
              ))}
          </div>
        );
      }
      if (content.type === "tech_stack")
        return <TechStackCloud data={content} />;
    }
    return (
      <ReactMarkdown
        components={{
          a: ({ ...props }) => (
            <a
              className="text-purple-400 underline hover:text-purple-300"
              target="_blank"
              rel="noopener noreferrer"
              {...props}
            />
          ),
        }}
      >
        {String(content)}
      </ReactMarkdown>
    );
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 left-4 bg-purple-600 text-white p-4 rounded-full shadow-lg transform hover:scale-110 transition-transform z-[1000]"
      >
        <FaCommentDots size={24} />
      </button>
      {isOpen && (
        <div className="fixed bottom-20 left-4 w-full max-w-md h-[70vh] bg-gray-100 dark:bg-gray-800 shadow-2xl rounded-lg flex flex-col z-[999]">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full flex items-center justify-center bg-purple-100 dark:bg-purple-900/50">
              <FaRobot
                className="text-purple-600 dark:text-purple-300"
                size={20}
              />
            </div>
            <div>
              <h3 className="font-bold text-lg text-gray-900 dark:text-gray-100">
                AI Career Assistant
              </h3>
            </div>
          </div>
          <div className="flex-1 p-4 overflow-y-auto space-y-6">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex items-start gap-2.5 ${
                  msg.role === "user" ? "flex-row-reverse" : "flex-row"
                }`}
              >
                <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gray-300 dark:bg-gray-600">
                  <FaUser size={14} />
                </div>
                <div
                  className={`max-w-xs md:max-w-sm p-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-purple-600 text-white"
                      : "bg-white dark:bg-gray-700 shadow-sm"
                  }`}
                >
                  {renderMessageContent(msg.content)}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            {messages.length <= 1 && (
              <div className="flex flex-wrap gap-2 mb-3">
                {suggestedPrompts.map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(prompt)}
                    disabled={isLoading}
                    className="px-3 py-1 bg-gray-200 dark:bg-gray-700 text-sm rounded-full hover:bg-purple-200 dark:hover:bg-purple-800 transition-colors disabled:opacity-50"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            )}
            <form
              onSubmit={handleFormSubmit}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 p-2.5 rounded-full px-4 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none"
                placeholder="Ask a question..."
                disabled={isLoading}
              />
              <button
                type="submit"
                className="w-10 h-10 flex items-center justify-center bg-purple-600 text-white rounded-full hover:bg-purple-700 disabled:bg-gray-500"
                disabled={isLoading}
              >
                <FaPaperPlane />
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatAssistant;
