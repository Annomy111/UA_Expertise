"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';
import { Search, Menu, X, Database, Users, Building2, BarChart2, PlusCircle } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();
  const pathname = usePathname();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const navLinks = [
    { href: '/', label: 'Home', icon: <Database className="h-4 w-4 mr-1" /> },
    { href: '/experts', label: 'Individual Experts', icon: <Users className="h-4 w-4 mr-1" /> },
    { href: '/organizations', label: 'Organizations', icon: <Building2 className="h-4 w-4 mr-1" /> },
    { href: '/statistics', label: 'Statistics', icon: <BarChart2 className="h-4 w-4 mr-1" /> },
    { href: '/add', label: 'Add New', icon: <PlusCircle className="h-4 w-4 mr-1" /> },
  ];

  return (
    <nav className="bg-gradient-to-r from-blue-800 to-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="flex items-center">
                <span className="text-xl font-bold tracking-tight mr-2">🇺🇦</span>
                <div className="flex flex-col">
                  <span className="text-lg font-bold tracking-tight leading-tight">Anthony Richter Associates</span>
                  <span className="text-xs text-blue-200">Ukraine Experts Database</span>
                </div>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <form onSubmit={handleSearch} className="relative mr-4">
              <Input
                type="text"
                placeholder="Search experts..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 rounded-md text-black w-64 border-0 focus:ring-2 focus:ring-blue-400"
              />
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
            </form>
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  pathname === link.href 
                    ? 'bg-blue-900 text-white' 
                    : 'text-blue-100 hover:bg-blue-700 hover:text-white'
                }`}
              >
                {link.icon}
                {link.label}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleMenu}
              className="text-white hover:bg-blue-700"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        className={`${
          isMenuOpen ? 'block' : 'hidden'
        } md:hidden absolute top-16 left-0 right-0 bg-white shadow-md z-10`}
      >
        <div className="flex flex-col p-4 space-y-3">
          <form onSubmit={handleSearch} className="relative mb-3">
            <Input
              type="text"
              placeholder="Search experts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 rounded-md text-black w-full"
            />
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
          </form>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center px-3 py-2 rounded-md ${
                pathname === link.href
                  ? 'bg-blue-100 text-blue-800 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
              onClick={() => setIsMenuOpen(false)}
            >
              {link.icon}
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 