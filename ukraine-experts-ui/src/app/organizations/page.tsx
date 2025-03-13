"use client";

import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { getCities, getExpertsByCity, getDiasporaOrganizations, Expert, City } from '@/lib/api';
import Layout from '@/components/layout/Layout';
import ExpertsList from '@/components/experts/ExpertsList';
import { Button } from '@/components/ui/button';
import { Filter, X } from 'lucide-react';

// Wrapper-Komponente mit Suspense-Boundary
export default function OrganizationsPageWrapper() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <OrganizationsPage />
    </Suspense>
  );
}

// Hauptkomponente
function OrganizationsPage() {
  const searchParams = useSearchParams();
  const cityParam = searchParams.get('city');
  const diasporaParam = searchParams.get('diaspora');

  const [organizations, setOrganizations] = useState<Expert[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [selectedCity, setSelectedCity] = useState<string>(cityParam || '');
  const [showDiasporaOnly, setShowDiasporaOnly] = useState<boolean>(diasporaParam === 'true');
  const [showFilters, setShowFilters] = useState(false);

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
    const fetchOrganizations = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Initialize orgsData as an empty array
        let orgsData: Expert[] = [];
        
        // Fetch organizations based on city if provided, otherwise fetch all
        if (cityParam) {
          const response = await fetch(`http://localhost:8000/city/${cityParam}`);
          if (!response.ok) {
            throw new Error('Failed to fetch organizations by city');
          }
          orgsData = await response.json();
        } else {
          const response = await fetch('http://localhost:8000/search?q=');
          if (!response.ok) {
            throw new Error('Failed to fetch all organizations');
          }
          orgsData = await response.json();
        }
        
        // Filter for organizations
        orgsData = orgsData.filter(org => org.type === 'organization');
        
        // Further filter by diaspora parameter if set
        if (diasporaParam === 'true') {
          orgsData = orgsData.filter(org => org.is_diaspora);
        } else if (diasporaParam === 'false') {
          orgsData = orgsData.filter(org => !org.is_diaspora);
        }
        
        // Deduplicate organizations by ID and name
        const uniqueOrgs: Expert[] = [];
        const orgIds = new Set<string>();
        const orgNames = new Set<string>();
        
        for (const org of orgsData) {
          if (!orgIds.has(org.id) && !orgNames.has(org.name)) {
            orgIds.add(org.id);
            orgNames.add(org.name);
            uniqueOrgs.push(org);
          }
        }
        
        setOrganizations(uniqueOrgs);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching organizations:', err);
        setError('Failed to load organizations. Please try again later.');
        setLoading(false);
      }
    };
    
    fetchOrganizations();
  }, [cityParam, diasporaParam]);

  const applyFilters = () => {
    // Build the URL with query parameters
    const params = new URLSearchParams();
    
    if (selectedCity) {
      params.set('city', selectedCity);
    }
    
    if (showDiasporaOnly) {
      params.set('diaspora', 'true');
    }

    // Update the URL without reloading the page
    window.history.pushState({}, '', `${window.location.pathname}?${params.toString()}`);
    window.location.reload();
  };

  const clearFilters = () => {
    setSelectedCity('');
    setShowDiasporaOnly(false);
    window.history.pushState({}, '', window.location.pathname);
    window.location.reload();
  };

  const toggleFilters = () => {
    setShowFilters(!showFilters);
  };

  const getPageTitle = () => {
    if (diasporaParam === 'true') {
      return 'Diaspora Organizations';
    }
    
    if (cityParam) {
      const city = cities.find(c => c.id.toString() === cityParam);
      return city ? `Organizations in ${city.name}, ${city.country}` : 'Organizations by City';
    }
    
    return 'All Organizations';
  };

  return (
    <Layout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-6">{getPageTitle()}</h1>
        
        <div className="flex justify-between items-center mb-6">
          <p className="text-gray-600">
            Showing {organizations.length} organizations
            {cityParam && cities.find(c => c.id.toString() === cityParam) && 
              ` in ${cities.find(c => c.id.toString() === cityParam)?.name}`}
            {diasporaParam === 'true' && ' in the diaspora'}
          </p>
          
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
            
            {(selectedCity || showDiasporaOnly || cityParam || diasporaParam) && (
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
              
              <div className="flex items-end">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={showDiasporaOnly}
                    onChange={(e) => setShowDiasporaOnly(e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 mr-2"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    Show diaspora organizations only
                  </span>
                </label>
              </div>
            </div>
            
            <div className="mt-4 flex justify-end">
              <Button type="button" onClick={applyFilters}>
                Apply Filters
              </Button>
            </div>
          </div>
        )}
      
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading organizations...</p>
            </div>
          </div>
        ) : error ? (
          <div className="text-center py-10">
            <h2 className="text-xl font-bold text-red-600 mb-4">Error</h2>
            <p className="text-gray-700 mb-6">{error}</p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </div>
        ) : (
          <ExpertsList 
            experts={organizations} 
            title="" 
            emptyMessage="No organizations found matching your criteria. Try adjusting your filters."
          />
        )}
      </div>
    </Layout>
  );
} 