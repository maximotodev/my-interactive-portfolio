import React, { useState } from "react";
import { submitContactForm, submitNostrContactForm } from "../api";
import {
  FaPaperPlane,
  FaSpinner,
  FaCheckCircle,
  FaShieldAlt,
} from "react-icons/fa";
import FadeIn from "./FadeIn";

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [status, setStatus] = useState("idle");
  const [errors, setErrors] = useState({});
  const [sendViaNostr, setSendViaNostr] = useState(false); // <-- NEW state for the toggle

  const handleChange = (e) =>
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("sending");
    setErrors({});

    // Choose which API function to call based on the toggle state
    const submissionFunction = sendViaNostr
      ? submitNostrContactForm
      : submitContactForm;

    try {
      await submissionFunction(formData);
      setStatus("success");
    } catch (error) {
      setStatus("error");
      if (error.response && error.response.data) setErrors(error.response.data);
    }
  };

  if (status === "success") {
    return (
      <FadeIn>
        <div className="text-center p-8 bg-green-100 dark:bg-green-900/50 rounded-lg">
          <FaCheckCircle className="text-green-500 text-4xl mx-auto mb-4" />
          <h3 className="text-xl font-bold text-green-800 dark:text-green-200">
            Message Sent!
          </h3>
          <p className="text-green-700 dark:text-green-300">
            {sendViaNostr
              ? "Your encrypted message is on its way via Nostr."
              : "Thank you for reaching out. I'll get back to you shortly."}
          </p>
        </div>
      </FadeIn>
    );
  }

  return (
    <section className="my-12">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-900 dark:text-gray-100">
        Get In Touch
      </h2>
      <form
        onSubmit={handleSubmit}
        className="max-w-xl mx-auto p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl space-y-4"
      >
        {/* --- Form fields are unchanged --- */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium">
            Name
          </label>
          <input
            type="text"
            name="name"
            id="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-transparent focus:border-purple-500 focus:ring-purple-500"
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium">
            Email
          </label>
          <input
            type="email"
            name="email"
            id="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-transparent focus:border-purple-500 focus:ring-purple-500"
          />
          {errors.email && (
            <p className="text-sm text-red-500 mt-1">{errors.email}</p>
          )}
        </div>
        <div>
          <label htmlFor="subject" className="block text-sm font-medium">
            Subject
          </label>
          <input
            type="text"
            name="subject"
            id="subject"
            value={formData.subject}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-transparent focus:border-purple-500 focus:ring-purple-500"
          />
        </div>
        <div>
          <label htmlFor="message" className="block text-sm font-medium">
            Message
          </label>
          <textarea
            name="message"
            id="message"
            rows="4"
            value={formData.message}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-transparent focus:border-purple-500 focus:ring-purple-500"
          ></textarea>
        </div>

        {/* --- NEW: Nostr Toggle Switch --- */}
        <div className="flex items-center justify-center p-3 bg-purple-50 dark:bg-purple-900/30 rounded-lg">
          <label
            htmlFor="nostr-toggle"
            className="flex items-center cursor-pointer"
          >
            <div className="relative">
              <input
                type="checkbox"
                id="nostr-toggle"
                className="sr-only"
                checked={sendViaNostr}
                onChange={() => setSendViaNostr(!sendViaNostr)}
              />
              <div className="block bg-gray-300 dark:bg-gray-600 w-14 h-8 rounded-full"></div>
              <div className="dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform"></div>
            </div>
            <div className="ml-3 text-gray-700 dark:text-gray-300">
              <p className="font-semibold flex items-center gap-2">
                <FaShieldAlt className="text-purple-500" />
                Send via Nostr
              </p>
              <p className="text-xs">Sends as an end-to-end encrypted DM.</p>
            </div>
          </label>
        </div>
        {/* Simple CSS in JS for the toggle switch animation */}
        <style>{`#nostr-toggle:checked ~ .dot { transform: translateX(100%); }`}</style>

        <div>
          <button
            type="submit"
            disabled={status === "sending"}
            className="w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400"
          >
            {status === "sending" ? (
              <FaSpinner className="animate-spin" />
            ) : (
              <FaPaperPlane />
            )}
            {status === "sending" ? "Sending..." : "Send Message"}
          </button>
        </div>
        {status === "error" && (
          <p className="text-sm text-red-500 text-center">
            There was an issue sending your message. Please try again.
          </p>
        )}
      </form>
    </section>
  );
};

export default ContactForm;
