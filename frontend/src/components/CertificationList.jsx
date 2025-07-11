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
    <section className="my-8">
      <h2 className="text-3xl font-bold mb-6 border-b-2 border-purple-500 pb-2">
        Certifications
      </h2>
      <ul>
        {certs.map((cert) => (
          <li
            key={cert.id}
            className="bg-gray-800 p-4 rounded-lg mb-4 flex justify-between items-center"
          >
            <div>
              <p className="font-bold text-lg">{cert.name}</p>
              <p className="text-gray-400">
                {cert.issuing_organization} -{" "}
                {new Date(cert.date_issued).getFullYear()}
              </p>
            </div>
            <a
              href={cert.credential_url}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-1 px-3 rounded"
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
