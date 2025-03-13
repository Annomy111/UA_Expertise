import React from 'react';
import { Statistics } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Building2, MapPin, Tag } from 'lucide-react';

interface StatisticsOverviewProps {
  statistics: Statistics;
}

const StatisticsOverview: React.FC<StatisticsOverviewProps> = ({ statistics }) => {
  const totalExperts = 
    (statistics.by_type.individual || 0) + 
    (statistics.by_type.organization || 0);
  
  const totalDiaspora = statistics.by_diaspora.True || 0;
  
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Database Statistics</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Experts</CardTitle>
            <Users className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalExperts}</div>
            <p className="text-xs text-gray-500 mt-1">
              {statistics.by_type.individual || 0} individuals, {statistics.by_type.organization || 0} organizations
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Diaspora Organizations</CardTitle>
            <Building2 className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalDiaspora}</div>
            <p className="text-xs text-gray-500 mt-1">
              {Math.round((totalDiaspora / totalExperts) * 100)}% of total experts
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Cities Represented</CardTitle>
            <MapPin className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{statistics.by_city.length}</div>
            <p className="text-xs text-gray-500 mt-1">
              Across {new Set(statistics.by_city.map(city => city.country)).size} countries
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Top Focus Area</CardTitle>
            <Tag className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold capitalize">
              {statistics.by_focus_area[0]?.focus_area.replace('_', ' ')}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {statistics.by_focus_area[0]?.count} experts
            </p>
          </CardContent>
        </Card>
      </div>
      
      {/* Detailed Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* By City */}
        <Card>
          <CardHeader>
            <CardTitle>Experts by City</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {statistics.by_city.map((city) => (
                <div key={city.name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <MapPin className="h-4 w-4 mr-2 text-gray-500" />
                    <span>
                      {city.name}, {city.country}
                    </span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-32 h-2 bg-gray-200 rounded-full mr-2">
                      <div
                        className="h-2 bg-blue-600 rounded-full"
                        style={{
                          width: `${(city.count / Math.max(...statistics.by_city.map(c => c.count))) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm font-medium">{city.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        {/* By Focus Area */}
        <Card>
          <CardHeader>
            <CardTitle>Experts by Focus Area</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {statistics.by_focus_area.map((area) => (
                <div key={area.focus_area} className="flex items-center justify-between">
                  <span className="capitalize">
                    {area.focus_area.replace('_', ' ')}
                  </span>
                  <div className="flex items-center">
                    <div className="w-32 h-2 bg-gray-200 rounded-full mr-2">
                      <div
                        className="h-2 bg-blue-600 rounded-full"
                        style={{
                          width: `${(area.count / Math.max(...statistics.by_focus_area.map(a => a.count))) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm font-medium">{area.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
        
        {/* Top Tags */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Top Tags</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {statistics.top_tags.map((tag) => (
                <div
                  key={tag.name}
                  className="bg-gray-100 rounded-full px-3 py-1 text-sm flex items-center"
                >
                  <span>{tag.name}</span>
                  <span className="ml-2 bg-gray-200 rounded-full px-2 py-0.5 text-xs">
                    {tag.count}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default StatisticsOverview; 