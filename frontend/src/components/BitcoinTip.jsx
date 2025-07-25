// frontend/src/components/BitcoinTip.jsx
import React, { useState, useEffect } from "react";
import QRCode from "react-qr-code";
import { fetchBitcoinAddress } from "../api";
import Modal from "./Modal";

const BitcoinTip = () => {
  const [btcAddress, setBtcAddress] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copyText, setCopyText] = useState("Copy");

  useEffect(() => {
    const getAddress = async () => {
      try {
        const { data } = await fetchBitcoinAddress();
        setBtcAddress(data.address);
      } catch (error) {
        console.error("Could not fetch Bitcoin address from backend:", error);
      }
    };
    getAddress();
  }, []);

  const handleCopyAddress = () => {
    if (btcAddress) {
      navigator.clipboard.writeText(btcAddress);
      setCopyText("Copied!");
      setTimeout(() => setCopyText("Copy"), 2000);
    }
  };

  if (!btcAddress) {
    return null;
  }

  const qrValue = `bitcoin:${btcAddress}`;

  return (
    <>
      <button
        onClick={() => setIsModalOpen(true)}
        // Use a more generic orange color that works on both themes
        className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-6 rounded-lg transform hover:scale-105 active:scale-100"
      >
        <span>Zap sats ⚡</span>
      </button>

      {/* The Modal's own styles will be handled by its component file if needed */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        {/* Modal Content */}
        <h2 className="text-2xl font-bold mb-4 text-orange-500 dark:text-orange-400">
          Zap sats ⚡
        </h2>
        <p className="mb-4 text-gray-600 dark:text-gray-300">
          Scan with any Bitcoin wallet or copy the address.
        </p>

        <div className="bg-white p-4 inline-block rounded-lg">
          <QRCode
            value={qrValue}
            size={220}
            bgColor="#FFFFFF"
            fgColor="#000000"
          />
        </div>

        <div className="mt-4 p-3 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-between">
          <span className="text-sm font-mono break-all mr-2 text-gray-800 dark:text-gray-200">
            {btcAddress}
          </span>
          <button
            onClick={handleCopyAddress}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-1 px-3 rounded w-20 text-center"
            title="Copy to clipboard"
          >
            {copyText}
          </button>
        </div>
      </Modal>
    </>
  );
};

export default BitcoinTip;
