import React from 'react';
import { format } from 'date-fns';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  isPending?: boolean;
  error?: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  role, 
  content, 
  timestamp, 
  isPending = false,
  error 
}) => {
  const isUser = role === 'user';
  
  // Format timestamp if available
  const formattedTime = timestamp 
    ? format(new Date(timestamp), 'h:mm a') 
    : '';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div 
        className={`
          max-w-[80%] rounded-2xl px-4 py-3
          ${isUser 
            ? 'bg-primary text-primary-foreground rounded-br-none' 
            : 'bg-muted text-foreground rounded-bl-none'}
          ${error ? 'bg-destructive/20 border border-destructive' : ''}
        `}
      >
        {error ? (
          <div className="text-destructive">
            <p className="font-medium">Error: {error}</p>
            <p className="text-sm mt-1">Please try again or rephrase your request.</p>
          </div>
        ) : (
          <>
            <div className="whitespace-pre-wrap break-words">
              {isPending ? (
                <div className="flex items-center">
                  <span>{content}</span>
                  <span className="ml-2 flex space-x-1">
                    <span className="h-2 w-2 bg-current rounded-full animate-bounce"></span>
                    <span className="h-2 w-2 bg-current rounded-full animate-bounce delay-75"></span>
                    <span className="h-2 w-2 bg-current rounded-full animate-bounce delay-150"></span>
                  </span>
                </div>
              ) : (
                content
              )}
            </div>
            {formattedTime && (
              <div className={`text-xs mt-1 ${isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'}`}>
                {formattedTime}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;