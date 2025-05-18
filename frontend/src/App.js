import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { Layout, ExpertCard, Spinner, SearchInput, Select, Button, Badge } from './components/Layout';
import { fetchExperts, fetchCities, fetchStatistics } from './api';
import './App.css';

// Home page component
const Home = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    type: '',
    city_id: '',
    expertise: '',
  });

  // Fetch experts data
  const { data: experts, isLoading: expertsLoading } = useQuery(
    ['experts', search, filters],
    () => fetchExperts({ 
      search, 
      ...filters,
      limit: 12 
    }),
    { 
      keepPreviousData: true,
      staleTime: 5000
    }
  );

  // Fetch cities for filter
  const { data: cities } = useQuery('cities', fetchCities, {
    staleTime: 60000
  });

  // Fetch statistics
  const { data: statistics } = useQuery('statistics', fetchStatistics, {
    staleTime: 60000
  });

  // Extract unique expertise areas from experts data
  const expertiseAreas = React.useMemo(() => {
    if (!experts) return [];
    
    const areas = new Set();
    experts.forEach((expert) => {
      if (expert.expertise) {
        expert.expertise.forEach((area) => areas.add(area));
      }
    });
    
    return Array.from(areas).map(area => ({
      value: area,
      label: area
    }));
  }, [experts]);

  const handleSearchChange = (value) => {
    setSearch(value);
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleExpertClick = (expertId) => {
    navigate(`/experts/${expertId}`);
  };

  return (
    <div>
      {/* Hero Section */}
      <section className="hero-gradient py-20 px-4 text-white">
        <div className="container mx-auto text-center">
          <motion.h1 
            className="text-4xl md:text-6xl font-bold mb-6"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Ukraine Experts Database
          </motion.h1>
          <motion.p 
            className="text-xl mb-8 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Find Ukrainian experts and organizations across various fields and disciplines
          </motion.p>
          <motion.div 
            className="max-w-xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <SearchInput 
              value={search} 
              onChange={handleSearchChange} 
              placeholder="Search for experts, organizations, or expertise..."
            />
          </motion.div>
        </div>
      </section>

      {/* Filter Section */}
      <section className="bg-white shadow-md py-4 px-4">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
            <Select
              options={[
                { value: '', label: 'All Types' },
                { value: 'individual', label: 'Individuals' },
                { value: 'organization', label: 'Organizations' }
              ]}
              value={filters.type}
              onChange={(value) => handleFilterChange('type', value)}
              className="flex-1"
              placeholder="All Types"
            />
            <Select
              options={cities?.map(city => ({ 
                value: city.id, 
                label: `${city.name}, ${city.country}` 
              })) || []}
              value={filters.city_id}
              onChange={(value) => handleFilterChange('city_id', value)}
              className="flex-1"
              placeholder="All Locations"
            />
            <Select
              options={expertiseAreas}
              value={filters.expertise}
              onChange={(value) => handleFilterChange('expertise', value)}
              className="flex-1"
              placeholder="All Expertise Areas"
            />
            <Button 
              onClick={() => setFilters({ type: '', city_id: '', expertise: '' })}
              variant="secondary"
              className="md:self-end"
            >
              Reset Filters
            </Button>
          </div>
        </div>
      </section>

      {/* Experts Section */}
      <section className="py-12 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold mb-8 text-gray-800">Featured Experts & Organizations</h2>
          
          {expertsLoading ? (
            <div className="py-20">
              <Spinner />
            </div>
          ) : experts && experts.length > 0 ? (
            <motion.div 
              className="expert-card-grid"
              initial="hidden"
              animate="visible"
              variants={{
                hidden: { opacity: 0 },
                visible: {
                  opacity: 1,
                  transition: {
                    staggerChildren: 0.1
                  }
                }
              }}
            >
              {experts.map((expert) => (
                <motion.div 
                  key={expert.id}
                  variants={{
                    hidden: { opacity: 0, y: 20 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >
                  <ExpertCard expert={expert} onClick={() => handleExpertClick(expert.id)} />
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <div className="text-center py-10">
              <p className="text-gray-500 text-lg">No experts found matching your criteria.</p>
              <Button 
                onClick={() => {
                  setSearch('');
                  setFilters({ type: '', city_id: '', expertise: '' });
                }}
                className="mt-4"
              >
                Clear Filters
              </Button>
            </div>
          )}
        </div>
      </section>

      {/* Statistics Section */}
      {statistics && (
        <section className="py-12 px-4 bg-gray-50">
          <div className="container mx-auto">
            <h2 className="text-3xl font-bold mb-8 text-gray-800">Database Statistics</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card p-6">
                <h3 className="text-xl font-semibold mb-4">Total Entries</h3>
                <div className="text-4xl font-bold text-ukraine-blue">
                  {statistics.total_entries}
                </div>
                <div className="mt-4 flex space-x-4">
                  <div>
                    <div className="text-sm text-gray-500">Individuals</div>
                    <div className="text-xl font-semibold">{statistics.by_type.individual}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Organizations</div>
                    <div className="text-xl font-semibold">{statistics.by_type.organization}</div>
                  </div>
                </div>
              </div>
              
              <div className="card p-6">
                <h3 className="text-xl font-semibold mb-4">Top Locations</h3>
                <ul className="space-y-2">
                  {statistics.by_city.slice(0, 5).map((city) => (
                    <li key={city.city_id} className="flex justify-between items-center">
                      <span>
                        {city.name}, {city.country}
                      </span>
                      <Badge color="blue">{city.count}</Badge>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="card p-6">
                <h3 className="text-xl font-semibold mb-4">Top Expertise Areas</h3>
                <ul className="space-y-2">
                  {statistics.by_expertise.slice(0, 5).map((item) => (
                    <li key={item.expertise} className="flex justify-between items-center">
                      <span>{item.expertise}</span>
                      <Badge color="yellow">{item.count}</Badge>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="bg-ukraine-blue text-white py-16 px-4">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Are You an Expert on Ukraine?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join our database of Ukraine experts and organizations to connect with researchers, journalists, and policymakers worldwide.
          </p>
          <Button 
            variant="secondary" 
            className="text-lg px-8 py-3"
            onClick={() => navigate('/add')}
          >
            Join the Database
          </Button>
        </div>
      </section>
    </div>
  );
};

// Expert detail page (placeholder)
const ExpertDetail = () => {
  return (
    <div className="container mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-4">Expert Detail Page</h1>
      <p>This page would display detailed information about a specific expert.</p>
    </div>
  );
};

// Add expert page (placeholder)
const AddExpert = () => {
  return (
    <div className="container mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold mb-4">Add New Expert</h1>
      <p>This page would contain a form to add a new expert to the database.</p>
    </div>
  );
};

// Main App component
function App() {
  return (
    <AnimatePresence mode="wait">
      <Routes>
        <Route path="/" element={
          <Layout>
            <Home />
          </Layout>
        } />
        <Route path="/experts/:id" element={
          <Layout>
            <ExpertDetail />
          </Layout>
        } />
        <Route path="/add" element={
          <Layout>
            <AddExpert />
          </Layout>
        } />
      </Routes>
    </AnimatePresence>
  );
}

export default App;