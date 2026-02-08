'use client';

import { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const ChatInterface = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'assistant', content: 'Hello! I\'m your Todo AI Assistant. How can I help you manage your tasks today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Add event listener for ChatBubby button
  useEffect(() => {
    const handleOpenChat = () => {
      setIsOpen(true);
    };

    window.addEventListener('open-chatbubby', handleOpenChat);
    
    return () => {
      window.removeEventListener('open-chatbubby', handleOpenChat);
    };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get user ID from auth context
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('User not authenticated');
      }

      // Decode the JWT token to get user info
      const payload = JSON.parse(atob(token.split('.')[1]));
      const userId = payload.sub || payload.userId || 'unknown'; // Common JWT claim names

      // Make real HTTP request to backend API
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;
      if (!backendUrl) {
        throw new Error('NEXT_PUBLIC_BACKEND_API_URL environment variable is not defined');
      }

      const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Include auth token if needed
        },
        body: JSON.stringify({
          message: {
            role: 'user',
            content: inputValue
          },
          metadata: {
            timestamp: new Date().toISOString()
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // Add real assistant response from backend
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response.content || 'Received response from backend'
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `Error: ${error.message || 'Failed to process your request'}. Please try again.`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Indigo/Purple Floating Chat Icon */}
      <button
        onClick={toggleChat}
        className={`
          fixed bottom-6 right-6 w-14 h-14 rounded-full flex items-center justify-center shadow-lg
          transition-all duration-300 transform hover:scale-110 z-50
          ${isOpen ? 'bg-indigo-700' : 'bg-indigo-600'} text-white
          focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50
          group
          sm:bottom-6 sm:right-6
          md:bottom-6 md:right-6
        `}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {/* Glow effect ring */}
        <div className={`
          absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 
          transition-opacity duration-500
          bg-indigo-500 blur-md -z-10
        `}></div>
        
        {isOpen ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="white"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="white"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        )}
      </button>

      {/* White + Indigo/Purple Chat Modal */}
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-40 p-4 sm:p-0 sm:items-end sm:justify-end sm:mr-6 sm:mb-24">
          <div className="fixed inset-0 bg-black bg-opacity-30" onClick={toggleChat}></div>
          <div className="relative bg-white rounded-xl shadow-2xl flex flex-col w-full max-w-full h-[70vh] max-h-[600px] sm:w-[90vw] sm:max-w-md sm:h-[70vh] md:w-[70vw] md:max-w-md md:h-[70vh] lg:w-[28rem] lg:h-[500px] xl:h-[550px] border border-gray-200 overflow-hidden z-50">
            {/* Chat Header */}
            <header className="bg-indigo-600 text-white p-4 shadow-md flex justify-between items-center">
              <div>
                <h1 className="text-lg font-bold">Todo AI Assistant</h1>
                <p className="text-xs opacity-80">Manage your tasks with natural language</p>
              </div>
              <button
                onClick={toggleChat}
                className="text-white hover:text-gray-200 focus:outline-none"
                aria-label="Close chat"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </header>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[80%] px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-purple-50 text-gray-800 border border-gray-200'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    </div>
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-purple-50 text-gray-800 border border-gray-200 max-w-[80%] px-4 py-2 rounded-lg">
                      <div className="flex items-center">
                        <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce mr-1"></div>
                        <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce mr-1 delay-75"></div>
                        <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                        <span className="ml-2 text-sm">Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 p-4 bg-white">
              <form
                onSubmit={handleSubmit}
                className="flex flex-col sm:flex-row gap-2"
              >
                <input
                  value={inputValue}
                  placeholder="Type your task management request..."
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading || !inputValue.trim()}
                  className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto"
                >
                  Send
                </button>
              </form>

              {/* Example prompts */}
              <div className="mt-3 text-xs text-gray-500 flex flex-wrap gap-2">
                <span className="bg-gray-100 px-2 py-1 rounded">"Add groceries"</span>
                <span className="bg-gray-100 px-2 py-1 rounded">"Show tasks"</span>
                <span className="bg-gray-100 px-2 py-1 rounded">"Complete #1"</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatInterface;