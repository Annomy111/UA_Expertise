import React from 'react';
import { Expert } from '@/lib/api';
import ExpertCard from './ExpertCard';

interface ExpertsListProps {
  experts: Expert[];
  title?: string;
  emptyMessage?: string;
}

const ExpertsList: React.FC<ExpertsListProps> = ({
  experts,
  title = 'Experts',
  emptyMessage = 'No experts found',
}) => {
  if (!experts || experts.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold mb-6">{title}</h2>
        <p className="text-gray-500">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div>
      {title && <h2 className="text-2xl font-bold mb-6">{title}</h2>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {experts.map((expert) => (
          <ExpertCard key={expert.id} expert={expert} />
        ))}
      </div>
    </div>
  );
};

export default ExpertsList; 