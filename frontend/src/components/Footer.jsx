import React, { useState } from "react";
import { ChevronUp, X, Github, Linkedin } from "lucide-react";

const Footer = () => {
  const [modalType, setModalType] = useState(null);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const getModalContent = () => {
    switch (modalType) {
      case "about":
        return {
          title: "About NewsHub",
          body: "NewsHub is an advanced AI-powered news aggregator built to fetch, summarize, and deliver hyper-local news from 22 major Indian cities as well as national trending updates in real-time. By utilizing state-of-the-art LLM summarization, we verify and synthesize reports from multiple web resources to present objective, engaging, and neutral news coverage."
        };
      case "contact":
        return {
          title: "Contact Us",
          body: "Have queries, suggestions, or feedback? We'd love to hear from you. Feel free to contact our development team at prateek.agengg1110@gmail.com. You can also connect with us directly on LinkedIn or follow our latest updates on GitHub."
        };
      case "privacy":
        return {
          title: "Privacy Policy",
          body: "Your privacy is important to us. NewsHub does not track your location, store personal profiles, or share credentials with third parties. All search parameters are processed anonymously on our backend to serve dynamic city-specific news feeds."
        };
      default:
        return null;
    }
  };

  const activeModal = getModalContent();

  return (
    <footer className="bg-gray-800 text-white mt-12 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">NewsHub</h3>
            <p className="text-gray-400">
              Your trusted source for the latest local, national, and global news updates.
            </p>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => setModalType("about")}
                  className="text-gray-400 hover:text-white transition-colors duration-200 focus:outline-none"
                >
                  About Us
                </button>
              </li>
              <li>
                <button
                  onClick={() => setModalType("contact")}
                  className="text-gray-400 hover:text-white transition-colors duration-200 focus:outline-none"
                >
                  Contact
                </button>
              </li>
              <li>
                <button
                  onClick={() => setModalType("privacy")}
                  className="text-gray-400 hover:text-white transition-colors duration-200 focus:outline-none"
                >
                  Privacy Policy
                </button>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Follow Us</h3>
            <div className="flex flex-col space-y-3">
              <a
                href="https://github.com/Prateek-1110/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center text-gray-400 hover:text-white transition-colors duration-200"
              >
                <Github className="h-5 w-5 mr-2" />
                GitHub
              </a>
              <a
                href="https://www.linkedin.com/in/prateek1110/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center text-gray-400 hover:text-white transition-colors duration-200"
              >
                <Linkedin className="h-5 w-5 mr-2" />
                LinkedIn
              </a>
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-700 flex justify-between items-center">
          <p className="text-gray-400">
            &copy; 2026 NewsHub. All rights reserved.
          </p>
          <button
            onClick={scrollToTop}
            className="p-2 bg-gray-700 rounded-full hover:bg-gray-600 transition-colors duration-200 focus:outline-none"
          >
            <ChevronUp className="h-6 w-6" />
          </button>
        </div>
      </div>

      {activeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div className="bg-white text-gray-800 rounded-xl max-w-md w-full p-6 relative shadow-2xl border border-gray-200 animate-in fade-in zoom-in-95 duration-150">
            <button
              onClick={() => setModalType(null)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors p-1 rounded-full hover:bg-gray-100"
            >
              <X className="h-5 w-5" />
            </button>
            <h3 className="text-xl font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2">
              {activeModal.title}
            </h3>
            <p className="text-gray-650 leading-relaxed text-sm">
              {activeModal.body}
            </p>
            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setModalType(null)}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </footer>
  );
};

export default Footer;
