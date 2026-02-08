import './globals.css';
import { ReactNode } from 'react';
import ClientAppWrapper from './ClientAppWrapper';
import ChatInterfaceWrapper from './ChatInterfaceWrapper';

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <ClientAppWrapper>
          <div className="min-h-screen">
            {children}
          </div>
          <ChatInterfaceWrapper />
        </ClientAppWrapper>
      </body>
    </html>
  );
}