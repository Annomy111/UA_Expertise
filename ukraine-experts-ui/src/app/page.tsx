"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Statistics, City, Expert } from '@/lib/api';
import Layout from '@/components/layout/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, Users, Building2, ChevronRight, Search } from 'lucide-react';
import ExpertsList from '@/components/experts/ExpertsList';

// Define the Organization type
type Organization = {
  id: string;
  name: string;
  type: string;
  is_diaspora: boolean;
  city_id: number;
  title?: string;
  affiliation?: string;
  description?: string;
  image?: string;
};

export default function Home() {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [diasporaOrgs, setDiasporaOrgs] = useState<Organization[]>([]);
  const [featuredExperts, setFeaturedExperts] = useState<Organization[]>([]);
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // The API base URL for our deployed backend
  const API_URL = 'https://ukraine-experts-api.windsurf.build/api';

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch statistics
        const statsResponse = await fetch(`${API_URL}/statistics`);
        if (!statsResponse.ok) throw new Error('Failed to fetch statistics');
        const statsData = await statsResponse.json();
        setStatistics(statsData);

        // Fetch experts for search
        const orgsResponse = await fetch(`${API_URL}/experts`);
        if (!orgsResponse.ok) throw new Error('Failed to fetch experts');
        const orgsData = await orgsResponse.json();
        
        // Filter for diaspora organizations
        const diasporaOrgs = orgsData.filter(
          (org: Organization) => org.type === 'organization' && org.is_diaspora
        );
        
        // Deduplicate diaspora organizations by ID and name
        const uniqueOrgs: Organization[] = [];
        const orgIds = new Set<string>();
        const orgNames = new Set<string>();
        
        for (const org of diasporaOrgs) {
          if (!orgIds.has(org.id) && !orgNames.has(org.name)) {
            orgIds.add(org.id);
            orgNames.add(org.name);
            uniqueOrgs.push(org);
          }
        }
        
        setDiasporaOrgs(uniqueOrgs);
        
        // Get random featured experts
        const expertsResponse = await fetch(`${API_URL}/experts`);
        if (!expertsResponse.ok) throw new Error('Failed to fetch experts');
        const expertsData = await expertsResponse.json();
        
        // Filter to only include individuals
        const individualExperts = expertsData.filter(
          (expert: Expert) => expert.type === 'individual'
        );
        
        // Deduplicate experts by ID and name
        const uniqueExperts: Expert[] = [];
        const expertIds = new Set<string>();
        const expertNames = new Set<string>();
        
        for (const expert of individualExperts) {
          if (!expertIds.has(expert.id) && !expertNames.has(expert.name)) {
            expertIds.add(expert.id);
            expertNames.add(expert.name);
            uniqueExperts.push(expert);
          }
        }
        
        // Select 3 random experts
        const shuffled = [...uniqueExperts].sort(() => 0.5 - Math.random());
        setFeaturedExperts(shuffled.slice(0, 3) as Organization[]);
        
        // Fetch cities
        const citiesResponse = await fetch(`${API_URL}/cities`);
        if (!citiesResponse.ok) throw new Error('Failed to fetch cities');
        const citiesData = await citiesResponse.json();
        setCities(citiesData);
        
        setLoading(false);
      } catch (error: unknown) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to load data';
        console.error('Error fetching data:', error);
        setLoading(false);
        setError(errorMessage);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading data...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-6">{error}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Hero Section */}
      <section className="py-16 mb-12 bg-gradient-to-r from-blue-900 to-blue-700 -mx-4 px-4 rounded-b-3xl shadow-lg text-white">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="text-5xl">🇺🇦</div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
            Ukraine Experts Database
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-10 max-w-3xl mx-auto">
            A comprehensive resource connecting Ukrainian experts and organizations across Europe
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/experts">
              <Button size="lg" className="gap-2 bg-white text-blue-800 hover:bg-blue-50">
                <Users className="h-5 w-5" />
                Individual Experts
              </Button>
            </Link>
            <Link href="/organizations">
              <Button size="lg" variant="outline" className="gap-2 border-white text-white hover:bg-blue-800">
                <Building2 className="h-5 w-5" />
                Organizations
              </Button>
            </Link>
            <Link href="/search">
              <Button size="lg" variant="outline" className="gap-2 border-white text-white hover:bg-blue-800">
                <Search className="h-5 w-5" />
                Search Database
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Overview */}
      {statistics && (
        <section className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Database Overview</h2>
            <Link href="/statistics">
              <Button variant="ghost" className="gap-1">
                View All Statistics
                <ChevronRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="border-t-4 border-t-blue-600 hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <Users className="h-5 w-5 mr-2 text-blue-600" />
                  Individual Experts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold mb-1">
                  {statistics.by_type.individual || 0}
                </div>
                <div className="text-sm text-gray-500">
                  Individual experts across Europe
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-t-4 border-t-blue-600 hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <Building2 className="h-5 w-5 mr-2 text-blue-600" />
                  Organizations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold mb-1">
                  {statistics.by_type.organization || 0}
                </div>
                <div className="text-sm text-gray-500">
                  Ukrainian organizations in Europe
                </div>
              </CardContent>
            </Card>
            
            <Card className="border-t-4 border-t-blue-600 hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg flex items-center">
                  <MapPin className="h-5 w-5 mr-2 text-blue-600" />
                  Cities
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold mb-1">
                  {statistics.by_city.length}
                </div>
                <div className="text-sm text-gray-500">
                  Across {new Set(statistics.by_city.map(city => city.country)).size} countries
                </div>
              </CardContent>
            </Card>
          </div>
        </section>
      )}

      {/* Featured Diaspora Organizations */}
      {diasporaOrgs.length > 0 && (
        <section className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Diaspora Organizations</h2>
            <Link href="/organizations" className="flex items-center text-blue-600 hover:text-blue-800">
              View all <ChevronRight className="h-4 w-4 ml-1" />
            </Link>
          </div>
          <ExpertsList 
            experts={diasporaOrgs.slice(0, 3) as any} 
            title="" 
          />
        </section>
      )}

      {/* Cities */}
      {cities.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold mb-6">Explore by City</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {cities.map((city) => (
              <Link key={city.id} href={`/experts?city=${city.id}`}>
                <Card className="hover:shadow-md transition-shadow cursor-pointer h-full border-l-4 border-l-blue-600">
                  <CardContent className="p-6">
                    <div className="flex items-center mb-2">
                      <MapPin className="h-4 w-4 mr-2 text-blue-600" />
                      <h3 className="font-medium">{city.name}</h3>
                    </div>
                    <p className="text-sm text-gray-500">{city.country}</p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      )}
    </Layout>
  );
}
