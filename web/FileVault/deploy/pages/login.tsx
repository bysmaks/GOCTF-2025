import { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (username && password) {
      const isValid = false;
      
      if (isValid) {
        document.cookie = 'authToken=valid_auth_token; path=/';
        router.push('/upload');
      } else {
        setError('Invalid credentials');
      }
    }
  };

  return (
    <Layout title="Login" showHeader={false}>
      <div className="flex justify-center items-center h-screen px-4">
        <div className="w-full max-w-md p-8 space-y-8 card">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-blue-400">FileVault</h1>
            <p className="text-gray-400 mt-1">Secure file sharing platform</p>
          </div>
          
          {error && (
            <div className="bg-red-900/50 text-red-300 p-3 rounded-lg text-sm border border-red-800">
              {error}
            </div>
          )}
          
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                required
              />
            </div>
            
            <div>
              <button
                type="submit"
                className="btn-primary w-full flex justify-center"
              >
                Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
} 