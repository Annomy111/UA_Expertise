import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from 'react-query';
import { motion } from 'framer-motion';
import { fetchCities, createExpert } from '../api';
import { Button, Select, Spinner } from '../components/Layout';

const AddExpert = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    type: 'individual',
    expertise: [],
    is_diaspora: false,
    title: '',
    affiliation: '',
    description: '',
    city_id: '',
    country: '',
    contact_email: '',
    contact_phone: '',
    website: '',
  });
  const [expertiseInput, setExpertiseInput] = useState('');
  const [formErrors, setFormErrors] = useState({});

  // Fetch cities for dropdown
  const { data: cities, isLoading: citiesLoading } = useQuery('cities', fetchCities, {
    staleTime: 60000
  });

  // Create expert mutation
  const mutation = useMutation(createExpert, {
    onSuccess: (data) => {
      navigate(`/experts/${data.id}`);
    },
    onError: (error) => {
      console.error('Error creating expert:', error);
      setFormErrors({ submit: 'Failed to create expert. Please try again.' });
    }
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error for this field if it exists
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleExpertiseAdd = () => {
    if (expertiseInput.trim()) {
      if (!formData.expertise.includes(expertiseInput.trim())) {
        setFormData(prev => ({
          ...prev,
          expertise: [...prev.expertise, expertiseInput.trim()]
        }));
      }
      setExpertiseInput('');
    }
  };

  const handleExpertiseRemove = (area) => {
    setFormData(prev => ({
      ...prev,
      expertise: prev.expertise.filter(item => item !== area)
    }));
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Name is required';
    }
    
    if (!formData.type) {
      errors.type = 'Type is required';
    }
    
    if (formData.contact_email && !/\S+@\S+\.\S+/.test(formData.contact_email)) {
      errors.contact_email = 'Invalid email format';
    }
    
    if (formData.website && !/^https?:\/\/.+\..+/.test(formData.website)) {
      errors.website = 'Website URL must start with http:// or https://';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      mutation.mutate(formData);
    }
  };

  return (
    <div className="container mx-auto py-12 px-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Add New Expert</h1>
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
        
        <div className="bg-white rounded-lg shadow-lg p-6">
          <form onSubmit={handleSubmit}>
            {formErrors.submit && (
              <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                {formErrors.submit}
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Basic Information */}
              <div>
                <h2 className="text-xl font-semibold mb-4 text-ukraine-blue border-b pb-2">Basic Information</h2>
                
                <div className="mb-4">
                  <label htmlFor="name" className="label">
                    Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    className={`input ${formErrors.name ? 'border-red-500' : ''}`}
                    value={formData.name}
                    onChange={handleInputChange}
                  />
                  {formErrors.name && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.name}</p>
                  )}
                </div>
                
                <div className="mb-4">
                  <label htmlFor="type" className="label">
                    Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="type"
                    name="type"
                    className={`input ${formErrors.type ? 'border-red-500' : ''}`}
                    value={formData.type}
                    onChange={handleInputChange}
                  >
                    <option value="individual">Individual</option>
                    <option value="organization">Organization</option>
                  </select>
                  {formErrors.type && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.type}</p>
                  )}
                </div>
                
                {formData.type === 'individual' && (
                  <div className="mb-4">
                    <label htmlFor="title" className="label">Title / Position</label>
                    <input
                      type="text"
                      id="title"
                      name="title"
                      className="input"
                      value={formData.title}
                      onChange={handleInputChange}
                      placeholder="e.g., Professor of Economics"
                    />
                  </div>
                )}
                
                <div className="mb-4">
                  <label htmlFor="affiliation" className="label">
                    {formData.type === 'individual' ? 'Affiliation' : 'Organization Type'}
                  </label>
                  <input
                    type="text"
                    id="affiliation"
                    name="affiliation"
                    className="input"
                    value={formData.affiliation}
                    onChange={handleInputChange}
                    placeholder={formData.type === 'individual' ? "e.g., University of Kyiv" : "e.g., NGO, Research Institute"}
                  />
                </div>
                
                <div className="mb-4">
                  <label htmlFor="description" className="label">Description</label>
                  <textarea
                    id="description"
                    name="description"
                    rows="4"
                    className="input"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Brief description..."
                  />
                </div>
                
                <div className="mb-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      name="is_diaspora"
                      checked={formData.is_diaspora}
                      onChange={handleInputChange}
                      className="mr-2"
                    />
                    <span>Part of Ukrainian diaspora</span>
                  </label>
                </div>
              </div>
              
              {/* Contact and Location */}
              <div>
                <h2 className="text-xl font-semibold mb-4 text-ukraine-blue border-b pb-2">Contact & Location</h2>
                
                <div className="mb-4">
                  <label htmlFor="city_id" className="label">City</label>
                  <select
                    id="city_id"
                    name="city_id"
                    className="input"
                    value={formData.city_id}
                    onChange={handleInputChange}
                    disabled={citiesLoading}
                  >
                    <option value="">Select a city</option>
                    {cities?.map(city => (
                      <option key={city.id} value={city.id}>
                        {city.name}, {city.country}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="mb-4">
                  <label htmlFor="country" className="label">Country</label>
                  <input
                    type="text"
                    id="country"
                    name="country"
                    className="input"
                    value={formData.country}
                    onChange={handleInputChange}
                    placeholder="Country (if city not listed above)"
                  />
                </div>
                
                <div className="mb-4">
                  <label htmlFor="contact_email" className="label">Email</label>
                  <input
                    type="email"
                    id="contact_email"
                    name="contact_email"
                    className={`input ${formErrors.contact_email ? 'border-red-500' : ''}`}
                    value={formData.contact_email}
                    onChange={handleInputChange}
                  />
                  {formErrors.contact_email && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.contact_email}</p>
                  )}
                </div>
                
                <div className="mb-4">
                  <label htmlFor="contact_phone" className="label">Phone</label>
                  <input
                    type="text"
                    id="contact_phone"
                    name="contact_phone"
                    className="input"
                    value={formData.contact_phone}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="mb-4">
                  <label htmlFor="website" className="label">Website</label>
                  <input
                    type="url"
                    id="website"
                    name="website"
                    className={`input ${formErrors.website ? 'border-red-500' : ''}`}
                    value={formData.website}
                    onChange={handleInputChange}
                    placeholder="https://..."
                  />
                  {formErrors.website && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.website}</p>
                  )}
                </div>
                
                <div className="mb-4">
                  <label htmlFor="expertise" className="label">Expertise Areas</label>
                  <div className="flex">
                    <input
                      type="text"
                      id="expertise"
                      className="input rounded-r-none"
                      value={expertiseInput}
                      onChange={(e) => setExpertiseInput(e.target.value)}
                      placeholder="Add expertise area..."
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleExpertiseAdd();
                        }
                      }}
                    />
                    <button
                      type="button"
                      className="px-4 bg-ukraine-blue text-white rounded-r-md hover:bg-blue-700"
                      onClick={handleExpertiseAdd}
                    >
                      Add
                    </button>
                  </div>
                  
                  <div className="mt-2 flex flex-wrap">
                    {formData.expertise.map((area, index) => (
                      <div 
                        key={index}
                        className="bg-blue-100 text-blue-800 rounded-full px-3 py-1 text-sm mr-2 mb-2 flex items-center"
                      >
                        {area}
                        <button
                          type="button"
                          className="ml-2 text-blue-500 hover:text-blue-700"
                          onClick={() => handleExpertiseRemove(area)}
                        >
                          &times;
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
            
            <div className="mt-8 flex justify-end">
              <Button 
                type="submit" 
                className="px-6 py-2"
                isLoading={mutation.isLoading}
                disabled={mutation.isLoading}
              >
                {mutation.isLoading ? 'Submitting...' : 'Add Expert'}
              </Button>
            </div>
          </form>
        </div>
      </motion.div>
    </div>
  );
};

export default AddExpert;
