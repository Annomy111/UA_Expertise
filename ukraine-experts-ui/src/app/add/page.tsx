"use client";

import React from 'react';
import Layout from '@/components/layout/Layout';
import { AddExpertForm } from '@/components/AddExpertForm';

export default function AddExpertPage() {
  return (
    <Layout>
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-8">Add New Expert or Organization</h1>
        <AddExpertForm onSuccess={() => {
          // This will be called after successful submission
          console.log('Expert/Organization added successfully');
        }} />
      </div>
    </Layout>
  );
} 