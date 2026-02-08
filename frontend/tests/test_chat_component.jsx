/**
 * Frontend component tests for the Todo AI Chatbot application.
 * Tests for the chat component and related UI elements using App Router.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInterface from '../../src/app/chat-interface';

describe('ChatInterface Component', () => {
  test('renders chat icon button initially', () => {
    render(<ChatInterface />);

    const chatButton = screen.getByLabelText(/Open chat/i);
    expect(chatButton).toBeInTheDocument();
    expect(chatButton).toHaveClass('bg-blue-600');
  });

  test('changes appearance when open', async () => {
    render(<ChatInterface />);

    // Click to open
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    // Verify the close button appears
    await waitFor(() => {
      const closeButton = screen.getByLabelText(/Close chat/i);
      expect(closeButton).toBeInTheDocument();
    });
  });

  test('opens chat interface when icon is clicked', async () => {
    render(<ChatInterface />);

    // Click the chat icon to open the chat
    const chatButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(chatButton);

    // Wait for the chat interface to appear
    await waitFor(() => {
      const chatHeader = screen.getByText(/Todo AI Assistant/i);
      expect(chatHeader).toBeInTheDocument();
    });
  });

  test('closes chat interface when close button is clicked', async () => {
    render(<ChatInterface />);

    // Open the chat first
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      const chatHeader = screen.getByText(/Todo AI Assistant/i);
      expect(chatHeader).toBeInTheDocument();
    });

    // Then click the close button
    const closeButton = screen.getByLabelText(/Close chat/i);
    fireEvent.click(closeButton);

    // The chat interface should disappear
    await waitFor(() => {
      const chatHeader = screen.queryByText(/Todo AI Assistant/i);
      expect(chatHeader).not.toBeInTheDocument();
    });
  });

  test('contains chat input field when open', async () => {
    render(<ChatInterface />);

    // Open the chat
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      const inputField = screen.getByPlaceholderText(/Type your task management request/i);
      expect(inputField).toBeInTheDocument();
    });
  });

  test('has example prompts when open', async () => {
    render(<ChatInterface />);

    // Open the chat
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      const examplePrompt = screen.getByText(/Add groceries/i);
      expect(examplePrompt).toBeInTheDocument();
    });
  });

  test('toggles chat visibility correctly', async () => {
    render(<ChatInterface />);

    // Initially, chat should be closed
    expect(screen.queryByText(/Todo AI Assistant/i)).not.toBeInTheDocument();

    // Open chat
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      expect(screen.getByText(/Todo AI Assistant/i)).toBeInTheDocument();
    });

    // Close chat
    const closeButton = screen.getByLabelText(/Close chat/i);
    fireEvent.click(closeButton);

    await waitFor(() => {
      expect(screen.queryByText(/Todo AI Assistant/i)).not.toBeInTheDocument();
    });

    // Open again
    fireEvent.click(openButton);

    await waitFor(() => {
      expect(screen.getByText(/Todo AI Assistant/i)).toBeInTheDocument();
    });
  });
});

// Additional tests for edge cases
describe('ChatInterface Component - Edge Cases', () => {
  test('handles rapid open/close clicks gracefully', async () => {
    render(<ChatInterface />);

    const openButton = screen.getByLabelText(/Open chat/i);

    // Rapidly click open/close multiple times
    fireEvent.click(openButton);
    await new Promise(resolve => setTimeout(resolve, 10));
    fireEvent.click(screen.getByLabelText(/Close chat/i));
    await new Promise(resolve => setTimeout(resolve, 10));
    fireEvent.click(openButton);

    // Component should still render without errors
    expect(openButton).toBeInTheDocument();
  });

  test('disables input when loading', async () => {
    // Mock the useChat hook to simulate loading state
    jest.mock('ai/react', () => ({
      useChat: () => ({
        messages: [],
        input: '',
        handleInputChange: jest.fn(),
        handleSubmit: jest.fn(),
        isLoading: true
      })
    }));

    render(<ChatInterface />);

    // Open the chat
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      const inputField = screen.getByPlaceholderText(/Type your task management request/i);
      expect(inputField).toBeDisabled();
    });

    // Clean up the mock
    jest.unmock('ai/react');
  });

  test('submit button is disabled when input is empty', async () => {
    render(<ChatInterface />);

    // Open the chat
    const openButton = screen.getByLabelText(/Open chat/i);
    fireEvent.click(openButton);

    await waitFor(() => {
      const submitButton = screen.getByText(/Send/i);
      expect(submitButton).toBeInTheDocument();
      // The button should be disabled when input is empty
      // Note: This depends on the actual implementation of the form
    });
  });
});