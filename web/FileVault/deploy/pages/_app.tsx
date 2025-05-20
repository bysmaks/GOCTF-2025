import { AppProps } from 'next/app';
import '../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className="fade-in">
      <Component {...pageProps} />
    </div>
  );
}

export default MyApp; 