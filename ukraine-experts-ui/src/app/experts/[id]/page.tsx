"use client";

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { getExpertDetails, searchExpertInfo, Expert } from '@/lib/api';
import Layout from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  MapPin, 
  Calendar, 
  Tag, 
  Mail, 
  Phone, 
  Globe, 
  Twitter, 
  Facebook, 
  Linkedin, 
  ArrowLeft,
  Building2,
  User,
  FileText,
  CalendarDays,
  Image as ImageIcon,
  Search,
  RefreshCw
} from 'lucide-react';

export default function ExpertDetailPage() {
  const params = useParams();
  const router = useRouter();
  const expertId = params.id as string;

  const [expert, setExpert] = useState<Expert | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imageError, setImageError] = useState(false);
  const [searchDescription, setSearchDescription] = useState<string | null>(null);
  const [searchLoading, setSearchLoading] = useState(false);

  useEffect(() => {
    const fetchExpertDetails = async () => {
      try {
        setLoading(true);
        const expertData = await getExpertDetails(expertId);
        console.log('Expert data received:', expertData);
        console.log('Description from API:', expertData.description);
        setExpert(expertData);
        
        if (!expertData.description) {
          console.log('Description is missing or empty, calling fetchAdditionalInfo.');
          fetchAdditionalInfo(expertData);
        } else {
          console.log('Description is present, not calling fetchAdditionalInfo.');
        }
      } catch (err) {
        console.error('Error fetching expert details:', err);
        setError('Failed to load expert details.');
      } finally {
        setLoading(false);
      }
    };

    if (expertId) {
      fetchExpertDetails();
    }
  }, [expertId]);

  const fetchAdditionalInfo = async (expertData: Expert) => {
    console.log('fetchAdditionalInfo called for:', expertData.name);
    try {
      setSearchLoading(true);
      setSearchDescription(null);
      const additionalInfo = await searchExpertInfo(expertData);
      console.log('Result from searchExpertInfo:', additionalInfo);
      setSearchDescription(additionalInfo);
    } catch (err) {
      console.error('Error fetching additional info:', err);
      setSearchDescription("Failed to perform research.");
    } finally {
      setSearchLoading(false);
    }
  };

  const goBack = () => {
    router.back();
  };

  const refreshResearchInfo = async () => {
    if (expert) {
      fetchAdditionalInfo(expert);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading expert details...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !expert) {
    return (
      <Layout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-6">{error || 'Failed to load expert details.'}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Back button */}
      <Button 
        variant="ghost" 
        onClick={goBack}
        className="flex items-center gap-2 mb-4"
      >
        <ArrowLeft className="h-4 w-4" />
        Back
      </Button>

      {/* Expert header section */}
      <div className="flex flex-col md:flex-row gap-6 mb-6 items-start">
        {/* Profile image */}
        {expert.image && (
          <div className="w-24 h-24 md:w-40 md:h-40 rounded-full bg-gray-100 flex-shrink-0 border-2 border-blue-500 shadow-md overflow-hidden">
            {!imageError ? (
              <img 
                src={expert.image} 
                alt={`${expert.name} profile`}
                className="w-full h-full object-cover"
                onError={() => setImageError(true)}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gray-200">
                <ImageIcon className="h-12 w-12 text-gray-400" />
              </div>
            )}
          </div>
        )}
        
        {/* Expert basic info */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h1 className="text-3xl font-bold">{expert.name}</h1>
            {expert.is_diaspora && (
              <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
                Diaspora
              </span>
            )}
          </div>
          
          <div className="flex items-center text-gray-600 mb-2">
            <MapPin className="h-4 w-4 mr-1" />
            {expert.city_name}, {expert.country}
          </div>
          
          <div className="flex items-center text-blue-700 mb-4">
            {expert.type === 'individual' ? (
              <>
                <User className="h-5 w-5 mr-2" />
                <span>Individual Expert</span>
              </>
            ) : (
              <>
                <Building2 className="h-5 w-5 mr-2" />
                <span>Organization</span>
              </>
            )}
          </div>
          
          {expert.type === 'individual' && expert.title && (
            <div className="mb-2">
              <span className="font-medium">Title:</span> {expert.title}
            </div>
          )}
          
          {expert.type === 'individual' && expert.affiliation && (
            <div className="mb-2">
              <span className="font-medium">Affiliation:</span> {expert.affiliation}
            </div>
          )}
          
          {expert.type === 'organization' && expert.founding_year && (
            <div className="mb-2">
              <span className="font-medium">Founded:</span> {expert.founding_year}
            </div>
          )}
        </div>
      </div>
      
      {/* Main content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column: About and Expertise */}
        <div className="lg:col-span-2 space-y-6">
          {/* About Section - Restore Research button and logic */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle>About</CardTitle>
              {/* Restore Research button */}
              <Button 
                variant="outline" 
                size="sm" 
                onClick={refreshResearchInfo}
                disabled={searchLoading}
                title="Refresh research information"
                className="flex items-center gap-1 text-xs"
              >
                {searchLoading ? 
                  <RefreshCw className="h-3 w-3 animate-spin" /> : 
                  <Search className="h-3 w-3" />
                }
                {searchLoading ? 'Researching...' : 'Research'}
              </Button>
            </CardHeader>
            <CardContent>
              {/* Original description if available */}
              {expert.description && (
                <div className="mb-4">
                  <h3 className="font-semibold mb-2">Description:</h3>
                  <p className="text-gray-700">{expert.description}</p>
                </div>
              )}
              
              {/* Research-based description if available */}
              {searchDescription && (
                <div className={expert.description ? "mt-6 pt-4 border-t border-gray-200" : ""}>
                  <div className="flex items-center mb-2">
                    <h3 className="font-semibold">Research Information:</h3>
                    {/* Optional: Add indicator if needed */}
                    {/* <span className="ml-2 text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">AI-enhanced</span> */}
                  </div>
                  <p className="text-gray-700">{searchDescription}</p>
                  {/* Optional: Add disclaimer if needed */}
                  {/* <p className="text-xs text-gray-500 mt-2 italic">...</p> */}
                </div>
              )}
              
              {/* If both are missing and search is in progress */}
              {!expert.description && searchLoading && (
                <div className="text-center py-6">
                  <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-blue-600" />
                  <p className="text-gray-600">Researching information about {expert.name}...</p>
                </div>
              )}
              
              {/* If both are missing and search is done but failed or no result */}
              {!expert.description && !searchLoading && !searchDescription && (
                 <p className="text-gray-500 italic">No description available</p>
                 // Button might be redundant if search is automatic, but kept for manual trigger
              )}
               {!expert.description && !searchLoading && searchDescription === "Failed to perform research." && (
                 <p className="text-red-500 italic">Failed to perform research.</p>
              )}
            </CardContent>
          </Card>
          
          {/* Research & Expertise Section - for individuals */}
          {expert.type === 'individual' && (
            <Card className="bg-blue-50 border-blue-200">
              <CardHeader className="bg-blue-100">
                <CardTitle>Research & Expertise</CardTitle>
              </CardHeader>
              <CardContent className="p-5">
                {/* Focus Areas */}
                {expert.focus_areas && expert.focus_areas.length > 0 ? (
                  <div className="mb-6">
                    <h3 className="font-semibold text-blue-800 mb-3">Focus Areas:</h3>
                    <div className="flex flex-wrap gap-2">
                      {expert.focus_areas.map((area) => (
                        <span
                          key={area}
                          className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {area.replace('_', ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 italic mb-6">No focus areas specified</p>
                )}
                
                {/* Tags */}
                {expert.tags && expert.tags.length > 0 ? (
                  <div>
                    <h3 className="font-semibold text-blue-800 mb-3">Tags:</h3>
                    <div className="flex flex-wrap gap-2">
                      {expert.tags.map((tag) => (
                        <span
                          key={tag}
                          className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 italic">No tags specified</p>
                )}
                
                {(!expert.focus_areas || expert.focus_areas.length === 0) && 
                 (!expert.tags || expert.tags.length === 0) && (
                  <p className="text-gray-500 italic">No research areas or tags available for this expert</p>
                )}
              </CardContent>
            </Card>
          )}
          
          {/* Focus Areas & Tags for organizations */}
          {expert.type === 'organization' && (
            <Card>
              <CardHeader>
                <CardTitle>Focus Areas & Tags</CardTitle>
              </CardHeader>
              <CardContent>
                {/* Focus Areas */}
                {expert.focus_areas && expert.focus_areas.length > 0 && (
                  <div className="mb-4">
                    <h3 className="font-semibold mb-2">Focus Areas:</h3>
                    <div className="flex flex-wrap gap-2">
                      {expert.focus_areas.map((area) => (
                        <span
                          key={area}
                          className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
                        >
                          {area.replace('_', ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Tags */}
                {expert.tags && expert.tags.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">Tags:</h3>
                    <div className="flex flex-wrap gap-2">
                      {expert.tags.map((tag) => (
                        <span
                          key={tag}
                          className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {(!expert.focus_areas || expert.focus_areas.length === 0) && 
                 (!expert.tags || expert.tags.length === 0) && (
                  <p className="text-gray-500 italic">No focus areas or tags available</p>
                )}
              </CardContent>
            </Card>
          )}
        </div>
        
        <div className="space-y-6">
          {/* Contact Information */}
          {expert.contacts && expert.contacts.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Contact Information</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {expert.contacts.map((contact, index) => (
                    <li key={contact.id || index} className="flex items-start">
                      {/* Icons basierend auf contact.contact_type */}
                      {contact.contact_type === 'email' && <Mail className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      {contact.contact_type === 'phone' && <Phone className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      {contact.contact_type === 'website' && <Globe className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      {contact.contact_type === 'twitter' && <Twitter className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      {contact.contact_type === 'facebook' && <Facebook className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      {contact.contact_type === 'linkedin' && <Linkedin className="h-5 w-5 mr-2 text-gray-500 mt-0.5" />}
                      
                      <div>
                        <div className="font-medium capitalize">{contact.contact_type}</div>
                        {/* Links/Text basierend auf contact.contact_type */}
                        {contact.contact_type === 'email' && (
                          <a href={`mailto:${contact.contact_value}`} className="text-blue-600 hover:underline">
                            {contact.contact_value}
                          </a>
                        )}
                        {contact.contact_type === 'phone' && (
                          <a href={`tel:${contact.contact_value}`} className="text-blue-600 hover:underline">
                            {contact.contact_value}
                          </a>
                        )}
                        {(contact.contact_type === 'website' || 
                          contact.contact_type === 'twitter' || 
                          contact.contact_type === 'facebook' || 
                          contact.contact_type === 'linkedin') && (
                          <a 
                            href={contact.contact_value.startsWith('http') ? contact.contact_value : `https://${contact.contact_value}`}
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {contact.contact_value}
                          </a>
                        )}
                        {!['email', 'phone', 'website', 'twitter', 'facebook', 'linkedin'].includes(contact.contact_type) && (
                          <span>{contact.contact_value}</span>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </Layout>
  );
} 