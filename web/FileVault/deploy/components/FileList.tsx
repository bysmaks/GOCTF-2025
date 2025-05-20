import { useState, useEffect } from 'react';
import Link from 'next/link';

interface FileListProps {
  id: string;
}

const FileList = ({ id }: FileListProps) => {
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/list-files?id=${id}`);
        
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        
        const data = await response.json();
        setFiles(data.files || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load files');
        console.error('Failed to load files:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchFiles();
    }
  }, [id]);

  if (loading) {
    return <div className="flex justify-center p-4"><div className="loader">Loading...</div></div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error loading files: {error}</div>;
  }

  if (files.length === 0) {
    return <div className="p-4 text-gray-500">No files found in this archive.</div>;
  }

  return (
    <div className="rounded bg-white shadow p-4">
      <h2 className="text-lg font-medium mb-4">Files in Archive</h2>
      <ul className="divide-y divide-gray-200">
        {files.map((file, index) => (
          <li key={index} className="py-2">
            <Link
              href={`/api/files/${id}/${file}`}
              target="_blank"
              className="text-blue-600 hover:text-blue-800 hover:underline flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              {file}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList; 