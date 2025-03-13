"use client";

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { TextArea } from '@/components/ui/TextArea';
import { Select } from '@/components/ui/Select';
import { getCities, createExpert, FocusArea } from '@/lib/api';

interface AddExpertFormProps {
  onSuccess: () => void;
}

export const AddExpertForm: React.FC<AddExpertFormProps> = ({ onSuccess }) => {
  const [cities, setCities] = useState<{ id: number; name: string; country: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const [formData, setFormData] = useState({
    name: '',
    type: 'organization' as 'individual' | 'organization',
    title: '',
    affiliation: '',
    city_id: 0,
    description: '',
    founding_year: undefined as number | undefined,
    is_diaspora: false,
    focus_areas: [] as FocusArea[],
    contacts: [] as { type: string; value: string; is_primary: boolean }[],
    key_figures: [] as { name: string; role: string; description: string }[],
    tags: [] as string[],
    image: '',
  });

  // New contact and key figure states
  const [newContact, setNewContact] = useState({ type: 'email', value: '', is_primary: false });
  const [newKeyFigure, setNewKeyFigure] = useState({ name: '', role: '', description: '' });
  const [newTag, setNewTag] = useState('');

  useEffect(() => {
    const fetchCities = async () => {
      try {
        const citiesData = await getCities();
        setCities(citiesData);
      } catch (err) {
        setError('Failed to load cities');
        console.error(err);
      }
    };

    fetchCities();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (name === 'city_id') {
      setFormData(prev => ({ ...prev, [name]: parseInt(value) }));
    } else if (name === 'founding_year' && value) {
      setFormData(prev => ({ ...prev, [name]: parseInt(value) }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleFocusAreaToggle = (area: FocusArea) => {
    setFormData(prev => {
      const areas = [...prev.focus_areas];
      if (areas.includes(area)) {
        return { ...prev, focus_areas: areas.filter(a => a !== area) };
      } else {
        return { ...prev, focus_areas: [...areas, area] };
      }
    });
  };

  const addContact = () => {
    if (newContact.value.trim()) {
      setFormData(prev => ({
        ...prev,
        contacts: [...prev.contacts, { ...newContact }]
      }));
      setNewContact({ type: 'email', value: '', is_primary: false });
    }
  };

  const removeContact = (index: number) => {
    setFormData(prev => ({
      ...prev,
      contacts: prev.contacts.filter((_, i) => i !== index)
    }));
  };

  const addKeyFigure = () => {
    if (newKeyFigure.name.trim()) {
      setFormData(prev => ({
        ...prev,
        key_figures: [...prev.key_figures, { ...newKeyFigure }]
      }));
      setNewKeyFigure({ name: '', role: '', description: '' });
    }
  };

  const removeKeyFigure = (index: number) => {
    setFormData(prev => ({
      ...prev,
      key_figures: prev.key_figures.filter((_, i) => i !== index)
    }));
  };

  const addTag = () => {
    if (newTag.trim() && !formData.tags.includes(newTag.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()]
      }));
      setNewTag('');
    }
  };

  const removeTag = (tag: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(t => t !== tag)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      await createExpert(formData);
      setSuccess(true);
      setFormData({
        name: '',
        type: 'organization',
        title: '',
        affiliation: '',
        city_id: 0,
        description: '',
        founding_year: undefined,
        is_diaspora: false,
        focus_areas: [],
        contacts: [],
        key_figures: [],
        tags: [],
        image: '',
      });
      onSuccess();
    } catch (err) {
      setError('Failed to create expert/organization');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const focusAreas: FocusArea[] = [
    'advocacy', 'humanitarian', 'cultural_diplomacy', 
    'political_mobilization', 'research', 'policy_analysis', 
    'community_support', 'integration', 'education', 'media'
  ];

  return (
    <Card className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Add New Expert/Organization</h2>
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          Expert/Organization added successfully!
        </div>
      )}
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block mb-2">Name *</label>
            <Input
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              placeholder="Organization or expert name"
            />
          </div>
          
          <div>
            <label className="block mb-2">Type *</label>
            <Select
              name="type"
              value={formData.type}
              onChange={handleInputChange}
              required
            >
              <option value="organization">Organization</option>
              <option value="individual">Individual</option>
            </Select>
          </div>
        </div>
        
        {formData.type === 'individual' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block mb-2">Title</label>
              <Input
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Professional title"
              />
            </div>
            
            <div>
              <label className="block mb-2">Affiliation</label>
              <Input
                name="affiliation"
                value={formData.affiliation}
                onChange={handleInputChange}
                placeholder="Organization affiliation"
              />
            </div>
          </div>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block mb-2">City *</label>
            <Select
              name="city_id"
              value={formData.city_id}
              onChange={handleInputChange}
              required
            >
              <option value={0}>Select a city</option>
              {cities.map(city => (
                <option key={city.id} value={city.id}>
                  {city.name}, {city.country}
                </option>
              ))}
            </Select>
          </div>
          
          {formData.type === 'organization' && (
            <div>
              <label className="block mb-2">Founding Year</label>
              <Input
                name="founding_year"
                type="number"
                value={formData.founding_year || ''}
                onChange={handleInputChange}
                placeholder="Year founded"
              />
            </div>
          )}
        </div>
        
        <div className="mb-4">
          <label className="block mb-2">Image URL</label>
          <Input
            name="image"
            value={formData.image}
            onChange={handleInputChange}
            placeholder="URL to profile/logo image"
          />
          <p className="text-sm text-gray-500 mt-1">Provide a URL to an image for this expert/organization</p>
        </div>
        
        <div className="mb-4">
          <label className="block mb-2">Description *</label>
          <TextArea
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            required
            rows={4}
            placeholder="Detailed description"
          />
        </div>
        
        <div className="mb-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_diaspora"
              checked={formData.is_diaspora}
              onChange={(e) => setFormData(prev => ({ ...prev, is_diaspora: e.target.checked }))}
              className="mr-2"
            />
            <span>Diaspora Organization/Expert</span>
          </label>
        </div>
        
        <div className="mb-6">
          <label className="block mb-2">Focus Areas</label>
          <div className="flex flex-wrap gap-2">
            {focusAreas.map(area => (
              <button
                key={area}
                type="button"
                onClick={() => handleFocusAreaToggle(area)}
                className={`px-3 py-1 rounded text-sm ${
                  formData.focus_areas.includes(area)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                {area.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
        
        {/* Contacts Section */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Contacts</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
            <div>
              <label className="block mb-1">Type</label>
              <Select
                value={newContact.type}
                onChange={(e) => setNewContact(prev => ({ ...prev, type: e.target.value }))}
              >
                <option value="email">Email</option>
                <option value="phone">Phone</option>
                <option value="website">Website</option>
                <option value="social">Social Media</option>
              </Select>
            </div>
            
            <div>
              <label className="block mb-1">Value</label>
              <Input
                value={newContact.value}
                onChange={(e) => setNewContact(prev => ({ ...prev, value: e.target.value }))}
                placeholder="Contact information"
              />
            </div>
            
            <div className="flex items-end">
              <Button type="button" onClick={addContact} className="mb-1">
                Add Contact
              </Button>
            </div>
          </div>
          
          {formData.contacts.length > 0 && (
            <div className="mt-2 border rounded p-2">
              <h4 className="font-medium mb-2">Added Contacts:</h4>
              <ul className="space-y-1">
                {formData.contacts.map((contact, index) => (
                  <li key={index} className="flex justify-between items-center">
                    <span>
                      {contact.type}: {contact.value}
                    </span>
                    <button
                      type="button"
                      onClick={() => removeContact(index)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
        
        {/* Key Figures Section (for organizations) */}
        {formData.type === 'organization' && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Key Figures</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
              <div>
                <label className="block mb-1">Name</label>
                <Input
                  value={newKeyFigure.name}
                  onChange={(e) => setNewKeyFigure(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Person's name"
                />
              </div>
              
              <div>
                <label className="block mb-1">Role</label>
                <Input
                  value={newKeyFigure.role}
                  onChange={(e) => setNewKeyFigure(prev => ({ ...prev, role: e.target.value }))}
                  placeholder="Position/role"
                />
              </div>
              
              <div className="flex items-end">
                <Button type="button" onClick={addKeyFigure} className="mb-1">
                  Add Key Figure
                </Button>
              </div>
            </div>
            
            <div>
              <label className="block mb-1">Description</label>
              <Input
                value={newKeyFigure.description}
                onChange={(e) => setNewKeyFigure(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Brief description"
              />
            </div>
            
            {formData.key_figures.length > 0 && (
              <div className="mt-2 border rounded p-2">
                <h4 className="font-medium mb-2">Added Key Figures:</h4>
                <ul className="space-y-2">
                  {formData.key_figures.map((figure, index) => (
                    <li key={index} className="flex justify-between items-start">
                      <div>
                        <div className="font-medium">{figure.name}</div>
                        <div className="text-sm">{figure.role}</div>
                        {figure.description && (
                          <div className="text-sm text-gray-600">{figure.description}</div>
                        )}
                      </div>
                      <button
                        type="button"
                        onClick={() => removeKeyFigure(index)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
        
        {/* Tags Section */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Tags</h3>
          
          <div className="flex gap-2 mb-2">
            <Input
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="Add a tag"
              className="flex-grow"
              onKeyPress={(e: React.KeyboardEvent) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addTag();
                }
              }}
            />
            <Button type="button" onClick={addTag}>
              Add Tag
            </Button>
          </div>
          
          {formData.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {formData.tags.map(tag => (
                <span
                  key={tag}
                  className="bg-gray-200 px-2 py-1 rounded-full text-sm flex items-center"
                >
                  {tag}
                  <button
                    type="button"
                    onClick={() => removeTag(tag)}
                    className="ml-1 text-gray-600 hover:text-gray-800"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>
        
        <div className="flex justify-end">
          <Button type="submit" disabled={loading} className="px-6">
            {loading ? 'Submitting...' : 'Add Expert/Organization'}
          </Button>
        </div>
      </form>
    </Card>
  );
}; 