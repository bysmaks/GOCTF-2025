import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const authCookie = request.cookies.get('authToken');
  
  if (request.nextUrl.pathname === '/' || 
      request.nextUrl.pathname.startsWith('/upload') || 
      request.nextUrl.pathname.startsWith('/api/upload') ||
      request.nextUrl.pathname.startsWith('/api/endpoints') ||
      request.nextUrl.pathname.startsWith('/api/files/') ||
      request.nextUrl.pathname.startsWith('/api/list-files')) {
    
    if (!authCookie || authCookie.value !== 'valid_auth_token') {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}