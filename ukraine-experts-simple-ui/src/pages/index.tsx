import { useState, useEffect } from 'react';
import axios from 'axios';

// API URL for our backend
const API_URL = 'https://ukraine-experts-api.windsurf.build/api';

// Simple types for our data
interface Expert {
  id: string;
  name: string;
  type: string;
  title?: string;
  affiliation?: string;
  city_id: number;
  is_diaspora: boolean;
  image?: string;
  city?: {
    name: string;
    country: string;
  };
}

interface Statistics {
  total_experts: number;
  experts_by_type: {
    individual: number;
    organization: number;
  };
  experts_by_country: Record<string, number>;
  top_cities: Array<{
    city: string;
    country: string;
    count: number;
  }>;
}

export default function Home() {
  const [experts, setExperts] = useState<Expert[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch experts
        const expertsResponse = await axios.get(`${API_URL}/experts`);
        setExperts(expertsResponse.data);

        // Fetch statistics
        const statsResponse = await axios.get(`${API_URL}/statistics`);
        setStatistics(statsResponse.data);

        setLoading(false);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch data');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Ukraine Experts Database</h1>
        <div className="text-center">Loading...</div>
      </div>
    </div>
  );

  if (error) return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Ukraine Experts Database</h1>
        <div className="text-center text-red-500">Error: {error}</div>
        <div className="mt-4 text-center">
          <p>Please make sure your backend API is running at: {API_URL}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Ukraine Experts Database</h1>
        
        {/* Statistics Section */}
        {statistics && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">Database Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500">Total Experts</p>
                <p className="text-2xl font-bold">{statistics.total_experts}</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500">Individuals</p>
                <p className="text-2xl font-bold">{statistics.experts_by_type.individual || 0}</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500">Organizations</p>
                <p className="text-2xl font-bold">{statistics.experts_by_type.organization || 0}</p>
              </div>
            </div>
            
            {/* Top Countries */}
            <h3 className="text-lg font-semibold mt-6 mb-3">Top Countries</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(statistics.experts_by_country)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 6)
                .map(([country, count]) => (
                  <div key={country} className="flex justify-between bg-gray-50 p-3 rounded">
                    <span>{country}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
            </div>
          </div>
        )}
        
        {/* Experts List */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Experts Directory</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {experts.slice(0, 9).map(expert => (
              <div key={expert.id} className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                <div className="p-4">
                  <h3 className="font-semibold text-lg truncate">{expert.name}</h3>
                  <p className="text-sm text-gray-500 capitalize">{expert.type}</p>
                  {expert.title && <p className="text-sm mt-1">{expert.title}</p>}
                  {expert.affiliation && <p className="text-sm text-gray-600">{expert.affiliation}</p>}
                </div>
              </div>
            ))}
          </div>
          
          {experts.length > 9 && (
            <div className="mt-6 text-center">
              <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
                View All Experts
              </button>
            </div>
          )}
        </div>
        
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Backend API: {API_URL}</p>
        </div>
      </div>
    </div>
  );
}
