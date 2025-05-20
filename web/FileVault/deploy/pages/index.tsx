import { useRouter } from 'next/router';
import Layout from '../components/Layout';

export default function Home() {
  const router = useRouter();

  const handleUpload = () => {
    router.push('/upload');
  };

  return (
    <Layout title="Welcome to FileVault">
      <div className="flex flex-col items-center justify-center h-screen px-4">
        <div className="max-w-md w-full space-y-8 text-center">
          <div>
            <h1 className="text-4xl font-bold text-blue-400">FileVault</h1>
            <p className="mt-2 text-gray-400">Secure file sharing platform</p>
          </div>
          
          <button
            onClick={handleUpload}
            className="btn-primary flex items-center justify-center mx-auto mt-8"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            Go to Upload
          </button>
        </div>
      </div>
    </Layout>
  );
} 