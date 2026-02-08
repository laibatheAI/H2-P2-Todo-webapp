'use client';

import { usePathname } from 'next/navigation';
import { useAuth } from '../lib/auth-context';
import ChatInterface from './chat-interface';

// Public routes where the chat icon should not appear
const PUBLIC_ROUTES = ['/', '/auth/login', '/auth/register'];

export default function ChatInterfaceWrapper() {
  const pathname = usePathname();
  const { isAuthenticated, loading } = useAuth();

  // Determine if the current route is public
  const isPublicRoute = PUBLIC_ROUTES.some(publicRoute => pathname === publicRoute || 
    (publicRoute !== '/' && pathname.startsWith(publicRoute + '/')));

  // Don't render anything while loading auth status
  if (loading) {
    return null;
  }

  // Render the chat interface if the user is authenticated (regardless of route, except public routes)
  if (isAuthenticated && !isPublicRoute) {
    return <ChatInterface />;
  }

  // Return null if not authenticated or on a public route
  return null;
}