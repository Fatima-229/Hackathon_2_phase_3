'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/components/AuthProvider';
import { useRouter } from 'next/navigation';
import { API_BASE_URL } from '../../constants/api';
import MessageBubble from '@/components/MessageBubble';
import ChatInput from '@/components/ChatInput';
import ChatHeader from '@/components/ChatHeader';

export default function ChatPage() {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, router]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
      isPending: true
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get token from localStorage
      const token = localStorage.getItem('token');

      if (!token) {
        throw new Error('No authentication token found');
      }

      // Extract user ID from token (JWT payload)
      let userId = user?.id;
      if (!userId) {
        // Decode the JWT token to get the user ID from the 'sub' claim
        const tokenPayload = token.split('.')[1];
        // Add padding if needed
        const base64 = tokenPayload.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const decodedToken = JSON.parse(jsonPayload);
        userId = decodedToken.sub; // 'sub' is typically the user identifier in JWT
      }

      if (!userId) {
        throw new Error('Unable to determine user ID');
      }

      // Send message to backend - using unified endpoint
      const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/api/v1/chat/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_message: message
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to send message' }));
        throw new Error(errorData.detail || 'Failed to send message');
      }

      const data = await response.json();

      // Update user message to remove pending state
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id
            ? { ...msg, isPending: false }
            : msg
        )
      );

      // Add AI response - now using the correct format
      const aiMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.assistant_message,
        timestamp: new Date().toISOString(),
        conversationId: data.conversation_id
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Update user message to show error
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id
            ? { ...msg, isPending: false, error: error.message }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null; // Render nothing while redirecting
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <ChatHeader title="AI Task Assistant" />
      
      <main className="flex-1 flex flex-col max-w-4xl w-full mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4 max-h-[calc(100vh-220px)]">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center py-12">
              <h2 className="text-2xl font-bold text-foreground mb-2">Welcome to AI Task Assistant!</h2>
              <p className="text-muted-foreground mb-6">
                I can help you manage your tasks. Try asking me to add, list, update, or complete tasks.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
                <div className="bg-card p-4 rounded-lg border border-border">
                  <p className="font-medium">Examples:</p>
                  <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                    <li>"Add a task to buy groceries"</li>
                    <li>"Show me my tasks"</li>
                  </ul>
                </div>
                <div className="bg-card p-4 rounded-lg border border-border">
                  <p className="font-medium">Capabilities:</p>
                  <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                    <li>Add, list, update tasks</li>
                    <li>Mark tasks as complete</li>
                    <li>Delete tasks</li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <MessageBubble
                key={message.id}
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
                isPending={message.isPending}
                error={message.error}
              />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <ChatInput 
          onSendMessage={handleSendMessage} 
          disabled={isLoading} 
        />
      </main>
    </div>
  );
}