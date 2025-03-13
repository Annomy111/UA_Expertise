import React from 'react';
import Navbar from './Navbar';
import { Github, Mail, Globe, Phone } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8 max-w-7xl">
        {children}
      </main>
      <footer className="bg-gray-800 text-white py-10 mt-12">
        <div className="container mx-auto px-4 max-w-7xl">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <span className="mr-2">🇺🇦</span> Ukraine Experts Database
              </h3>
              <p className="text-gray-300 text-sm">
                Connecting Ukrainian experts and organizations across Europe to foster collaboration and support.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <a href="/" className="text-gray-300 hover:text-white text-sm transition-colors">
                    Home
                  </a>
                </li>
                <li>
                  <a href="/experts" className="text-gray-300 hover:text-white text-sm transition-colors">
                    Individual Experts
                  </a>
                </li>
                <li>
                  <a href="/organizations" className="text-gray-300 hover:text-white text-sm transition-colors">
                    Organizations
                  </a>
                </li>
                <li>
                  <a href="/statistics" className="text-gray-300 hover:text-white text-sm transition-colors">
                    Statistics
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact</h3>
              <div className="mb-4">
                <p className="text-gray-300 text-sm font-medium">Anthony Richter Associates, Inc.</p>
                <ul className="space-y-2 mt-2">
                  <li className="flex items-center">
                    <Phone className="h-4 w-4 mr-2 text-gray-400" />
                    <a href="tel:+19176788300" className="text-gray-300 hover:text-white text-sm transition-colors">
                      +1 917 678 8300
                    </a>
                  </li>
                  <li className="flex items-center">
                    <Phone className="h-4 w-4 mr-2 text-gray-400" />
                    <a href="tel:+19177751187" className="text-gray-300 hover:text-white text-sm transition-colors">
                      +1 917 775-1187
                    </a>
                  </li>
                  <li className="flex items-center">
                    <Mail className="h-4 w-4 mr-2 text-gray-400" />
                    <a href="mailto:anthony.richter@richterassociates.net" className="text-gray-300 hover:text-white text-sm transition-colors">
                      anthony.richter@richterassociates.net
                    </a>
                  </li>
                </ul>
              </div>
              <ul className="space-y-2 border-t border-gray-700 pt-4">
                <li className="flex items-center">
                  <Github className="h-4 w-4 mr-2 text-gray-400" />
                  <a href="https://github.com/ukraine-experts" className="text-gray-300 hover:text-white text-sm transition-colors">
                    github.com/ukraine-experts
                  </a>
                </li>
                <li className="flex items-center">
                  <Globe className="h-4 w-4 mr-2 text-gray-400" />
                  <a href="https://ukraineexperts.org" className="text-gray-300 hover:text-white text-sm transition-colors">
                    ukraineexperts.org
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-6 flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-sm text-gray-400">
                &copy; {new Date().getFullYear()} Ukraine Experts Database. All rights reserved.
              </p>
            </div>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Privacy Policy
              </a>
              <a
                href="#"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Terms of Service
              </a>
              <a
                href="#"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout; 