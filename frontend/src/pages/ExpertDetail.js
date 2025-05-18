import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { fetchExpertById, fetchCities } from '../api';
import { Spinner, Button, Badge } from '../components/Layout';

const ExpertDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  // Fetch expert data
  const { data: expert, isLoading, error } = useQuery(
    ['expert', id],
    () => fetchExpertById(id),
    { staleTime: 5000 }
  );
  
  // Fetch cities for location data
  const { data: cities } = useQuery('cities', fetchCities, {
    staleTime: 60000
  });
  
  const getCityName = (cityId) => {
    if (!cities) return 'Unknown Location';
    const city = cities.find(c => c.id === cityId);
    return city ? `${city.name}, ${city.country}` : 'Unknown Location';
  };
  
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner />
      </div>
    );
  }
  
  if (error || !expert) {
    return (
      <div className="container mx-auto py-12 px-4 text-center">
        <h1 className="text-2xl font-bold text-red-600 mb-4">Error Loading Expert</h1>
        <p className="mb-6">There was a problem loading the expert information.</p>
        <Button onClick={() => navigate('/')}>Return to Home</Button>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto py-12 px-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex justify-between items-center mb-8">
          <Button 
            variant="secondary" 
            onClick={() => navigate(-1)}
            className="flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
            </svg>
            Back
          </Button>
        </div>
        
        <div className="bg-white rounded-lg shadow-xl overflow-hidden">
          <div className={`h-48 ${expert.type === 'individual' ? 'bg-ukraine-blue' : 'bg-ukraine-yellow'} relative`}>
            {expert.image ? (
              <img 
                src={expert.image} 
                alt={expert.name} 
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-white text-7xl font-bold">
                {expert.name.charAt(0)}
              </div>
            )}
            
            <div className="absolute bottom-0 left-0 w-full bg-black bg-opacity-50 text-white p-4">
              <div className="flex items-center">
                <Badge 
                  color={expert.type === 'individual' ? 'blue' : 'yellow'}
                >
                  {expert.type === 'individual' ? 'Expert' : 'Organization'}
                </Badge>
                {expert.is_diaspora && (
                  <Badge color="green">Diaspora</Badge>
                )}
              </div>
            </div>
          </div>
          
          <div className="p-6">
            <h1 className="text-3xl font-bold mb-2">{expert.name}</h1>
            {expert.title && (
              <p className="text-xl text-gray-600 mb-4">{expert.title}</p>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
              <div>
                <h2 className="text-xl font-semibold mb-4 text-ukraine-blue border-b pb-2">About</h2>
                {expert.description ? (
                  <p className="text-gray-700 mb-6">{expert.description}</p>
                ) : (
                  <p className="text-gray-500 italic mb-6">No description provided</p>
                )}
                
                {expert.affiliation && (
                  <div className="mb-4">
                    <h3 className="text-lg font-medium text-gray-800">Affiliation</h3>
                    <p className="text-gray-700">{expert.affiliation}</p>
                  </div>
                )}
                
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Expertise Areas</h3>
                  <div className="flex flex-wrap">
                    {expert.expertise && expert.expertise.length > 0 ? (
                      expert.expertise.map((area, index) => (
                        <span 
                          key={index} 
                          className="expertise-badge"
                        >
                          {area}
                        </span>
                      ))
                    ) : (
                      <p className="text-gray-500 italic">No expertise areas specified</p>
                    )}
                  </div>
                </div>
              </div>
              
              <div>
                <h2 className="text-xl font-semibold mb-4 text-ukraine-blue border-b pb-2">Contact Information</h2>
                <div className="space-y-4">
                  <div className="flex items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500 mr-3 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div>
                      <h3 className="text-lg font-medium text-gray-800">Location</h3>
                      <p className="text-gray-700">
                        {expert.city_id ? getCityName(expert.city_id) : (expert.country || 'Location not specified')}
                      </p>
                    </div>
                  </div>
                  
                  {expert.contact_email && (
                    <div className="flex items-start">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500 mr-3 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <div>
                        <h3 className="text-lg font-medium text-gray-800">Email</h3>
                        <a href={`mailto:${expert.contact_email}`} className="text-blue-600 hover:underline">
                          {expert.contact_email}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {expert.contact_phone && (
                    <div className="flex items-start">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500 mr-3 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <div>
                        <h3 className="text-lg font-medium text-gray-800">Phone</h3>
                        <a href={`tel:${expert.contact_phone}`} className="text-blue-600 hover:underline">
                          {expert.contact_phone}
                        </a>
                      </div>
                    </div>
                  )}
                  
                  {expert.website && (
                    <div className="flex items-start">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500 mr-3 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h.5A2.5 2.5 0 0020 5.5v-1.565M10 20a2 2 0 002 2h6a2 2 0 002-2V8a2 2 0 00-2-2H8a2 2 0 00-2 2" />
                      </svg>
                      <div>
                        <h3 className="text-lg font-medium text-gray-800">Website</h3>
                        <a href={expert.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                          {expert.website}
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ExpertDetail;
