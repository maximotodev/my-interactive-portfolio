// frontend/src/components/CertificationList.jsx
import React, { useState, useEffect } from "react";
import { fetchCertifications } from "../api";
import LoadingSpinner from "./LoadingSpinner";

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

  if (isLoading) return <LoadingSpinner />;

  return (
    <section className="my-12">
      <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2 text-gray-900 dark:text-gray-100">
        Certifications
      </h2>
      <ul className="space-y-4">
        {certs.map((cert) => (
          <li
            key={cert.id}
            className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md flex justify-between items-center ring-1 ring-black/5 dark:ring-white/10"
          >
            <div>
              <p className="font-bold text-lg text-gray-800 dark:text-gray-200">
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
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transform hover:scale-105 active:scale-100"
            >
              View
            </a>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default CertificationList;
