'use client';

import React, { useEffect, useState } from 'react';
import { getStatistics, Statistics } from '@/lib/api';
import Layout from '@/components/layout/Layout';
import StatisticsOverview from '@/components/statistics/StatisticsOverview';
import { Button } from '@/components/ui/button';

export default function StatisticsPage() {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        setLoading(true);
        const statsData = await getStatistics();
        setStatistics(statsData);
      } catch (err) {
        console.error('Error fetching statistics:', err);
        setError('Failed to load statistics data.');
      } finally {
        setLoading(false);
      }
    };

    fetchStatistics();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading statistics...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error || !statistics) {
    return (
      <Layout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-6">{error || 'Failed to load statistics.'}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <StatisticsOverview statistics={statistics} />
    </Layout>
  );
} 