import Head from 'next/head';
import { useRouter } from 'next/router';
import { ReactNode } from 'react';

type LayoutProps = {
  children: ReactNode;
  title: string;
  showHeader?: boolean;
  showFooter?: boolean;
};

export default function Layout({ children, title, showHeader = true, showFooter = true }: LayoutProps) {
  const router = useRouter();
  
  const handleLogout = () => {
    document.cookie = 'authToken=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      <Head>
        <title>{title} - FileVault</title>
        <meta name="description" content="Secure file sharing platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {showHeader && (
        <header className="bg-gray-800 p-4 shadow-md">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <h1 
              onClick={() => router.push('/')}
              className="text-xl font-bold text-blue-400 cursor-pointer hover:text-blue-300 transition-colors duration-200"
            >
              FileVault
            </h1>
            {router.pathname !== '/login' && (
              <nav className="space-x-4">
                <button
                  onClick={() => router.push('/upload')}
                  className="text-sm text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Upload
                </button>
                <button
                  onClick={handleLogout}
                  className="text-sm text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Logout
                </button>
              </nav>
            )}
          </div>
        </header>
      )}

      <main className="flex-grow">
        {children}
      </main>

      {showFooter && (
        <footer className="bg-gray-800 py-4 mt-auto">
          <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
            <p>FileVault - Secure file sharing platform</p>
            <p className="text-xs mt-1">© {new Date().getFullYear()} All rights reserved</p>
          </div>
        </footer>
      )}
    </div>
  );
} 