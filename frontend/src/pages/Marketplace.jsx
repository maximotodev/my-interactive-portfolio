// frontend/src/pages/Marketplace.jsx
import React, { useState, useEffect } from "react";
import { fetchProducts, fetchNostrProfile } from "../api/index";
import FadeIn from "../components/FadeIn";
import ImageWithFallback from "../components/ImageWithFallback";
import Pagination from "../components/Pagination";
import Modal from "../components/Modal";
import { FaUserCircle } from "react-icons/fa";

const PAGE_SIZE = 12;
// --- UPDATED HELPER FUNCTION ---
const formatPrice = (price, currency) => {
  if (price === null || price === undefined) return "N/A";
  if (price === 0) return "Free";
  // Use the currency from the product data
  try {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency || "USD",
    }).format(price);
  } catch (e) {
    // Fallback if currency code is invalid
    return `${price} ${currency}`;
  }
};

const truncatePubkey = (pubkey) => {
  if (!pubkey) return "";
  return `${pubkey.substring(0, 10)}...${pubkey.substring(pubkey.length - 4)}`;
};

const Marketplace = () => {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [sellerProfile, setSellerProfile] = useState(null);
  const [isProfileLoading, setIsProfileLoading] = useState(false);

  useEffect(() => {
    const abortController = new AbortController();
    const getProducts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await fetchProducts(currentPage, {
          signal: abortController.signal,
        });
        if (data && Array.isArray(data.results)) {
          setProducts(data.results);
          setTotalPages(Math.ceil(data.count / 12));
        } else {
          setProducts([]);
          setTotalPages(0);
        }
      } catch (err) {
        if (err.name !== "CanceledError") {
          setError("Failed to load products. Please try again later.");
        }
      } finally {
        if (!abortController.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    getProducts();
    return () => abortController.abort();
  }, [currentPage]);

  const handleCardClick = async (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
    setIsProfileLoading(true);
    try {
      // --- FIX: Use the correct pubkey field ---
      const { data } = await fetchNostrProfile(product.merchant_pubkey);
      setSellerProfile(data);
    } catch (error) {
      console.error("Failed to fetch seller profile:", error);
      setSellerProfile(null);
    } finally {
      setIsProfileLoading(false);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
    setSellerProfile(null);
  };
  if (isLoading) {
    // Skeleton Loader
    return (
      <div className="container mx-auto p-4 md:p-8">
        <header className="text-center mb-12 animate-pulse">
          <div className="h-10 bg-gray-300 dark:bg-gray-700 rounded-md w-1/2 mx-auto"></div>
          <div className="h-6 bg-gray-200 dark:bg-gray-600 rounded-md w-2/3 mx-auto mt-4"></div>
        </header>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[...Array(PAGE_SIZE)].map((_, i) => (
            <div
              key={i}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-80 animate-pulse"
            >
              <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded-t-lg"></div>
              <div className="p-6">
                <div className="h-6 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mt-2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Now we can properly display the error message
  if (error) return <p className="text-center mt-12 text-red-500">{error}</p>;

  return (
    <FadeIn>
      <div className="container mx-auto p-4 md:p-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">
            Nostr Marketplace
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">
            A curated feed of products and services from the global Nostr
            network.
          </p>
        </header>
        {products.length === 0 ? (
          <p className="text-center text-gray-500">
            No valid products found yet. The backend listener is warming up!
          </p>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.map((product) => (
                <button
                  key={product.event_id}
                  onClick={() => handleCardClick(product)}
                  className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 hover:-translate-y-1.5 hover:shadow-2xl hover:ring-2 hover:ring-purple-500 flex flex-col text-left"
                >
                  <ImageWithFallback
                    // --- FIX: Use the 'images' array ---
                    src={product.images && product.images[0]}
                    // --- FIX: Use the 'name' field ---
                    alt={product.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-6 flex-grow flex flex-col">
                    <h2
                      className="text-xl font-bold text-gray-800 dark:text-gray-200 truncate"
                      // --- FIX: Use the 'name' field ---
                      title={product.name}
                    >
                      {product.name}
                    </h2>
                    <p
                      className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-mono"
                      // --- FIX: Use the 'merchant_pubkey' field ---
                      title={product.merchant_pubkey}
                    >
                      by {truncatePubkey(product.merchant_pubkey)}
                    </p>
                    <div className="flex-grow"></div>
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                      <p className="text-2xl font-bold text-purple-600 dark:text-purple-400 text-right">
                        {/* --- FIX: Use the new price and currency fields --- */}
                        {formatPrice(product.price, product.currency)}
                      </p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </div>

      {/* --- MODAL DIALOG --- */}
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        {selectedProduct && (
          <div>
            <ImageWithFallback
              src={selectedProduct.images && selectedProduct.images[0]}
              alt={selectedProduct.name}
              className="w-full h-64 object-cover rounded-lg mb-4"
            />
            <h2 className="text-3xl font-bold mb-2">{selectedProduct.name}</h2>
            <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-900 rounded-lg">
              <h3 className="text-sm font-bold text-gray-600 dark:text-gray-400 mb-2">
                Seller Information
              </h3>
              {isProfileLoading ? (
                // ... (loader)
                <p>Loading profile...</p>
              ) : sellerProfile ? (
                <div className="flex items-center space-x-3">
                  <img
                    src={sellerProfile.picture}
                    alt={sellerProfile.name}
                    className="w-10 h-10 rounded-full"
                  />
                  <div>
                    <p className="font-bold">
                      {sellerProfile.name || sellerProfile.display_name}
                    </p>
                    <p className="text-xs text-gray-500 font-mono">
                      {truncatePubkey(selectedProduct.merchant_pubkey)}
                    </p>
                  </div>
                </div>
              ) : (
                // ... (fallback)
                <p>Could not load profile.</p>
              )}
            </div>
            <p className="text-gray-700 dark:text-gray-300 mb-4 whitespace-pre-wrap">
              {selectedProduct.description}
            </p>
            <div className="text-right">
              <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">
                {formatPrice(selectedProduct.price, selectedProduct.currency)}
              </p>
            </div>
          </div>
        )}
      </Modal>
    </FadeIn>
  );
};

export default Marketplace;
