import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import path from 'path';
import fs from 'fs';
import Layout from '../../components/Layout';
import FileList from '../../components/FileList';

export default function FilePage({ fileExists, files = [] }) {
  const router = useRouter();
  const { id } = router.query;
  
  if (!fileExists) {
    return (
      <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center">
        <Head>
          <title>FileVault - File Not Found</title>
        </Head>
        <div className="bg-gray-800 p-8 rounded-xl shadow-lg max-w-md w-full text-center">
          <h1 className="text-2xl font-bold text-red-400 mb-4">File Not Found</h1>
          <p className="text-gray-300 mb-6">The requested file could not be found.</p>
          <button
            onClick={() => router.push('/upload')}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Back to Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <Layout title={`Archive - ${id}`}>
      <Head>
        <title>Archive Files - {id}</title>
      </Head>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Archive Contents</h1>
          <p className="text-gray-600">ID: {id}</p>
        </div>

        {id && typeof id === 'string' && (
          <FileList id={id} />
        )}

        <div className="mt-8">
          <button 
            onClick={() => router.push('/upload')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Upload Another File
          </button>
        </div>
      </div>
    </Layout>
  );
}

export async function getServerSideProps({ params }) {
  const { id } = params;
  
  const sanitizedId = path.basename(id);
  const extractDir = path.join(process.cwd(), 'public', 'uploads', sanitizedId);
  
  try {
    const stats = fs.statSync(extractDir);
    
    if (stats.isDirectory()) {
      const files = fs.readdirSync(extractDir);
      return {
        props: {
          fileExists: true,
          files,
        },
      };
    }
  } catch (error) {
  }
  
  return {
    props: {
      fileExists: false,
    },
  };
} 