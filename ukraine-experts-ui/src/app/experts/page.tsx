"use client";

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { getCities, getExpertsByCity, getExpertsByFocus, searchExperts, Expert, City } from '@/lib/api';
import Layout from '@/components/layout/Layout';
import ExpertsList from '@/components/experts/ExpertsList';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Filter, X } from 'lucide-react';

// Wrapper-Komponente mit Suspense-Boundary
export default function ExpertsPageWrapper() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ExpertsPage />
    </Suspense>
  );
}

// Hauptkomponente
function ExpertsPage() {
  const searchParams = useSearchParams();
  const cityParam = searchParams.get('city');
  const focusParam = searchParams.get('focus');
  const queryParam = searchParams.get('q');

  const [experts, setExperts] = useState<Expert[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [searchQuery, setSearchQuery] = useState(queryParam || '');
  const [selectedCity, setSelectedCity] = useState<string>(cityParam || '');
  const [selectedFocus, setSelectedFocus] = useState<string>(focusParam || '');
  const [showFilters, setShowFilters] = useState(false);

  const focusAreas = [
    { value: 'advocacy', label: 'Advocacy' },
    { value: 'humanitarian', label: 'Humanitarian' },
    { value: 'cultural_diplomacy', label: 'Cultural Diplomacy' },
    { value: 'political_mobilization', label: 'Political Mobilization' },
    { value: 'research', label: 'Research' },
    { value: 'policy_analysis', label: 'Policy Analysis' },
    { value: 'community_support', label: 'Community Support' },
    { value: 'integration', label: 'Integration' },
    { value: 'education', label: 'Education' },
    { value: 'media', label: 'Media' },
  ];
  
  useEffect(() => {
    const fetchCities = async () => {
      try {
        const citiesData = await getCities();
        setCities(citiesData);
      } catch (err) {
        console.error('Error fetching cities:', err);
        setError('Failed to load cities data.');
      }
    };

    fetchCities();
  }, []);
  
  useEffect(() => {
    const fetchExperts = async () => {
      try {
        setLoading(true);
        let expertsData: Expert[] = [];

        if (queryParam) {
          expertsData = await searchExperts(queryParam);
        } else if (cityParam) {
          expertsData = await getExpertsByCity(parseInt(cityParam));
        } else if (focusParam) {
          expertsData = await getExpertsByFocus(focusParam);
        } else {
          // Fetch all experts from all cities
          const citiesData = await getCities();
          const allExpertsPromises = citiesData.map(city => getExpertsByCity(city.id));
          const expertsArrays = await Promise.all(allExpertsPromises);
          expertsData = expertsArrays.flat();
        }

        // Filter to only include individuals
        expertsData = expertsData.filter(expert => expert.type === 'individual');
        
        // Deduplicate experts by ID and name
        const uniqueExperts: Expert[] = [];
        const expertIds = new Set<string>();
        const expertNames = new Set<string>();
        
        for (const expert of expertsData) {
          // Only add if we haven't seen this ID or name before
          if (!expertIds.has(expert.id) && !expertNames.has(expert.name)) {
            expertIds.add(expert.id);
            expertNames.add(expert.name);
            uniqueExperts.push(expert);
          }
        }
        
        setExperts(uniqueExperts);
      } catch (err) {
        console.error('Error fetching experts:', err);
        setError('Failed to load experts data.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchExperts();
  }, [cityParam, focusParam, queryParam]);
  
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchQuery.trim() && !selectedCity && !selectedFocus) {
      return;
    }

    try {
      setLoading(true);
      let expertsData: Expert[] = [];
      
      // Build the URL with query parameters
      const params = new URLSearchParams(window.location.search);
      
      if (searchQuery.trim()) {
        params.set('q', searchQuery);
        expertsData = await searchExperts(searchQuery);
      } else {
        params.delete('q');
      }
      
      if (selectedCity) {
        params.set('city', selectedCity);
        if (!searchQuery.trim()) {
          expertsData = await getExpertsByCity(parseInt(selectedCity));
        }
      } else {
        params.delete('city');
      }
      
      if (selectedFocus) {
        params.set('focus', selectedFocus);
        if (!searchQuery.trim() && !selectedCity) {
          expertsData = await getExpertsByFocus(selectedFocus);
        }
      } else {
        params.delete('focus');
      }
      
      // Update the URL without reloading the page
      window.history.pushState({}, '', `${window.location.pathname}?${params.toString()}`);
      
      // Filter to only include individuals
      expertsData = expertsData.filter(expert => expert.type === 'individual');
      
      // Deduplicate experts by ID and name
      const uniqueExperts: Expert[] = [];
      const expertIds = new Set<string>();
      const expertNames = new Set<string>();
      
      for (const expert of expertsData) {
        // Only add if we haven't seen this ID or name before
        if (!expertIds.has(expert.id) && !expertNames.has(expert.name)) {
          expertIds.add(expert.id);
          expertNames.add(expert.name);
          uniqueExperts.push(expert);
        }
      }
      
      setExperts(uniqueExperts);
    } catch (err) {
      console.error('Error searching experts:', err);
      setError('Failed to search experts.');
    } finally {
      setLoading(false);
    }
  };
  
  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCity('');
    setSelectedFocus('');
    window.history.pushState({}, '', window.location.pathname);
    window.location.reload();
  };
  
  const toggleFilters = () => {
    setShowFilters(!showFilters);
  };

  const getPageTitle = () => {
    if (queryParam) {
      return `Individual Experts for "${queryParam}"`;
    }
    
    if (cityParam) {
      const city = cities.find(c => c.id.toString() === cityParam);
      return city ? `Individual Experts in ${city.name}, ${city.country}` : 'Individual Experts by City';
    }
    
    if (focusParam) {
      const focus = focusAreas.find(f => f.value === focusParam);
      return focus ? `Individual Experts in ${focus.label}` : 'Individual Experts by Focus Area';
    }
    
    return 'Individual Experts';
  };

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-6">{getPageTitle()}</h1>
        
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <form onSubmit={handleSearch} className="flex-grow relative">
            <Input
              type="text"
              placeholder="Search individual experts by name, description, or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2"
            />
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
            <Button type="submit" className="absolute right-1 top-1">
              Search
            </Button>
          </form>
          
          <div className="flex gap-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={toggleFilters}
              className="flex items-center gap-2"
            >
              <Filter className="h-4 w-4" />
              Filters
            </Button>
            
            {(searchQuery || selectedCity || selectedFocus) && (
              <Button 
                type="button" 
                variant="ghost" 
                onClick={clearFilters}
                className="flex items-center gap-2"
              >
                <X className="h-4 w-4" />
                Clear
              </Button>
            )}
          </div>
        </div>
        
        {showFilters && (
          <div className="bg-gray-50 p-4 rounded-md mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  City
                </label>
                <select
                  value={selectedCity}
                  onChange={(e) => setSelectedCity(e.target.value)}
                  className="w-full rounded-md border border-gray-300 p-2"
                >
                  <option value="">All Cities</option>
                  {cities.map((city) => (
                    <option key={city.id} value={city.id.toString()}>
                      {city.name}, {city.country}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Focus Area
                </label>
                <select
                  value={selectedFocus}
                  onChange={(e) => setSelectedFocus(e.target.value)}
                  className="w-full rounded-md border border-gray-300 p-2"
                >
                  <option value="">All Focus Areas</option>
                  {focusAreas.map((focus) => (
                    <option key={focus.value} value={focus.value}>
                      {focus.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="mt-4 flex justify-end">
              <Button 
                type="button" 
                onClick={handleSearch}
                className="flex items-center gap-2"
              >
                <Search className="h-4 w-4" />
                Apply Filters
              </Button>
            </div>
          </div>
        )}
        
        {error && (
          <div className="bg-red-50 text-red-700 p-4 rounded-md mb-6">
            {error}
          </div>
        )}
        
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
              <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">Loading...</span>
            </div>
            <p className="mt-2 text-gray-600">Loading experts...</p>
          </div>
        ) : (
          <ExpertsList experts={experts} />
        )}
      </div>
    </Layout>
  );
} 