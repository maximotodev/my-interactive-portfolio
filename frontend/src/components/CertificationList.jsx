import React, { useState, useEffect } from "react";
import { fetchCertifications } from "../api";
import FadeIn from "./FadeIn"; // Ensure FadeIn is imported

const CertificationList = () => {
  const [certs, setCerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getCerts = async () => {
      try {
        const { data } = await fetchCertifications();
        setCerts(data);
      } catch (error) {
        console.error("Failed to fetch certifications:", error);
      } finally {
        setIsLoading(false);
      }
    };
    getCerts();
  }, []);

  // --- 1. SKELETON LOADER (INLINE VERSION) ---
  if (isLoading) {
    return (
      <section className="my-12">
        <div className="h-8 w-1/4 bg-gray-300 dark:bg-gray-700 rounded animate-pulse mb-6"></div>
        <div className="space-y-4">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="h-20 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md animate-pulse"
            ></div>
          ))}
        </div>
      </section>
    );
  }

  return (
    <section className="my-12">
      <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2 text-gray-900 dark:text-gray-100">
        Certifications
      </h2>
      <ul className="space-y-4">
        {certs.map(
          (
            cert,
            index // <-- Get index for staggering
          ) => (
            // --- 2. APPLY STAGGERING & HOVER EFFECTS ---
            <FadeIn key={cert.id} delay={index * 100}>
              <li className="group bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md flex justify-between items-center ring-1 ring-black/5 dark:ring-white/10 transition-all duration-300 hover:ring-purple-500 hover:shadow-lg">
                <div>
                  <p className="font-bold text-lg text-gray-800 dark:text-gray-200 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                    {cert.name}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    {cert.issuing_organization} -{" "}
                    {new Date(cert.date_issued).toLocaleDateString()}
                  </p>
                </div>
                <a
                  href={cert.credential_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-purple-600 group-hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transform transition-all group-hover:scale-105 active:scale-100"
                >
                  View
                </a>
              </li>
            </FadeIn>
          )
        )}
      </ul>
    </section>
  );
};

export default CertificationList;
