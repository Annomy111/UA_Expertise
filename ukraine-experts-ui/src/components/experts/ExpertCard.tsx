"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { MapPin, Tag, ExternalLink, User, Building2, Image as ImageIcon } from 'lucide-react';
import { Expert } from '@/lib/api';
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface ExpertCardProps {
  expert: Expert;
}

const ExpertCard: React.FC<ExpertCardProps> = ({ expert }) => {
  const [imageError, setImageError] = useState(false);

  return (
    <Card className="overflow-hidden hover:shadow-md transition-shadow">
      <CardHeader className="pb-2">
        <CardTitle className="text-xl line-clamp-1 mb-2">
          <Link 
            href={`/experts/${expert.id}`} 
            className="hover:text-blue-700 transition-colors duration-200"
          >
            {expert.name}
          </Link>
        </CardTitle>
        
        {/* Image Display */}
        {expert.image && (
          <div className="mt-2 flex justify-center">
            <div className="w-24 h-24 relative overflow-hidden rounded-full bg-gray-100">
              {!imageError ? (
                <img 
                  src={expert.image}
                  alt={`${expert.name} profile`} 
                  className="w-full h-full object-cover"
                  onError={() => setImageError(true)}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-200">
                  <ImageIcon className="h-10 w-10 text-gray-400" />
                </div>
              )}
            </div>
          </div>
        )}
        
        <CardDescription className="flex items-center text-gray-600 mt-2 mb-1">
          <MapPin className="h-4 w-4 mr-1 flex-shrink-0" />
          <span className="truncate">{expert.city_name}, {expert.country}</span>
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        {/* Expert Type */}
        <div className="flex items-center text-blue-700 text-sm font-medium mb-3">
          {expert.type === 'individual' ? (
            <>
              <User className="h-4 w-4 mr-1" />
              <span>Individual Expert</span>
            </>
          ) : (
            <>
              <Building2 className="h-4 w-4 mr-1" />
              <span>Organization</span>
            </>
          )}
          {expert.is_diaspora && (
            <span className="ml-2 inline-block bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded">
              Diaspora
            </span>
          )}
        </div>
        
        {/* Focus Areas - Limited */}
        {expert.focus_areas && expert.focus_areas.length > 0 && (
          <div className="mt-3">
            <div className="flex flex-wrap gap-1 overflow-hidden max-h-12">
              {expert.focus_areas.slice(0, 3).map((area) => (
                <span
                  key={area}
                  className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full text-xs"
                >
                  {area.replace('_', ' ')}
                </span>
              ))}
              {expert.focus_areas.length > 3 && (
                <span className="text-gray-500 text-xs">+{expert.focus_areas.length - 3} more</span>
              )}
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Link href={`/experts/${expert.id}`} className="w-full">
          <Button variant="outline" className="w-full">
            View Details <ExternalLink className="h-3 w-3 ml-1" />
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
};

export default ExpertCard; 