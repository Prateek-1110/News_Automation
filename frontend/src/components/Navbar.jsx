import React, { useState } from "react";
import { Newspaper, ChevronDown } from "lucide-react";

const Navbar = ({ selectedCity, onCityChange }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const predefinedCities = [
    "All",
    "Delhi",
    "Mumbai",
    "Pune",
    "Lucknow",
    "Bengaluru",
    "Hyderabad",
    "Kolkata",
    "Chennai",
    "Ahmedabad",
    "Jaipur",
    "Surat",
    "Patna",
    "Kanpur",
    "Nagpur",
    "Indore",
    "Bhopal",
    "Visakhapatnam",
    "Vadodara",
    "Ghaziabad",
    "Ludhiana",
    "Agra",
    "Nashik"
  ];

  return (
    <nav className="sticky top-0 bg-white shadow-md z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Newspaper className="h-8 w-8 text-blue-600" />
            <span className="ml-2 text-xl font-bold text-gray-800">
              NewsHub
            </span>
          </div>

          <div className="relative">
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200 focus:outline-none"
            >
              {selectedCity === "All" ? "Select Location" : `City: ${selectedCity}`}
              <ChevronDown
                className={`ml-2 h-4 w-4 transition-transform duration-200 ${
                  isDropdownOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50 max-h-80 overflow-y-auto border border-gray-150">
                {predefinedCities.map((city, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      onCityChange(city);
                      setIsDropdownOpen(false);
                    }}
                    className={`block w-full text-left px-4 py-2 text-sm transition-colors duration-150 ${
                      selectedCity === city
                        ? "bg-blue-50 text-blue-600 font-semibold"
                        : "text-gray-700 hover:bg-gray-100"
                    }`}
                  >
                    {city === "All" ? "Trending (All)" : city}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
