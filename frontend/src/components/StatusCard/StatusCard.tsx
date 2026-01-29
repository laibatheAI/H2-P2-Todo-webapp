'use client';

import { useState, useEffect } from 'react';

interface StatusCardProps {
  title?: string;
  type: 'confirm' | 'success' | 'error'; 
  message: string;
  status: 'confirm' | 'success' | 'error';
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  onDismiss?: () => void;
  showActions?: boolean;
  showDismiss?: boolean;
  autoDismiss?: boolean;
  autoDismissDelay?: number;
}

export default function StatusCard({
  title = 'Confirmation',
  message,
  status,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  onDismiss,
  showActions = true,
  showDismiss = false,
  autoDismiss = false,
  autoDismissDelay = 3000
}: StatusCardProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (autoDismiss && status === 'success') {
      const timer = setTimeout(() => {
        setIsVisible(false);
        if (onDismiss) onDismiss();
      }, autoDismissDelay);

      return () => clearTimeout(timer);
    }
  }, [autoDismiss, autoDismissDelay, status, onDismiss]);

  if (!isVisible) return null;

  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return 'border-green-500/30 bg-green-500/5 dark:bg-green-900/20';
      case 'error':
        return 'border-red-500/30 bg-red-500/5 dark:bg-red-900/20';
      case 'confirm':
        return 'border-indigo-500/30 bg-indigo-500/5 dark:bg-indigo-900/20';
      default:
        return 'border-indigo-500/30 bg-indigo-500/5 dark:bg-indigo-900/20';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'success':
        return (
          <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        );
      case 'error':
        return (
          <div className="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        );
      case 'confirm':
        return (
          <div className="w-12 h-12 bg-indigo-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onCancel || (() => setIsVisible(false))}
      ></div>

      <div className={`relative bg-white dark:bg-slate-800/80 backdrop-blur-lg rounded-2xl shadow-2xl border ${getStatusColor()} max-w-md w-full p-6 transform transition-all duration-300 scale-100`}>
        {showDismiss && (
          <button
            onClick={() => {
              setIsVisible(false);
              if (onDismiss) onDismiss();
            }}
            className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}

        <div className="text-center">
          {getStatusIcon()}

          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            {title}
          </h3>

          <p className="text-gray-700 dark:text-gray-300 mb-6">
            {message}
          </p>

          {showActions && (
            <div className="flex flex-col sm:flex-row gap-3">
              {status === 'confirm' ? (
                <>
                  <button
                    onClick={() => {
                      if (onConfirm) onConfirm();
                    }}
                    className="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-medium rounded-lg hover:from-indigo-700 hover:to-indigo-800 transition-all duration-200 transform hover:scale-[1.02] shadow-lg shadow-indigo-500/20 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
                  >
                    {confirmText}
                  </button>
                  <button
                    onClick={() => {
                      if (onCancel) onCancel();
                    }}
                    className="flex-1 px-4 py-3 bg-gray-200 dark:bg-slate-700 text-gray-800 dark:text-gray-200 font-medium rounded-lg hover:bg-gray-300 dark:hover:bg-slate-600 transition-all duration-200"
                  >
                    {cancelText}
                  </button>
                </>
              ) : (
                <button
                  onClick={() => {
                    setIsVisible(false);
                    if (onDismiss) onDismiss();
                  }}
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-medium rounded-lg hover:from-indigo-700 hover:to-indigo-800 transition-all duration-200 transform hover:scale-[1.02] shadow-lg shadow-indigo-500/20 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
                >
                  Close
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}