import React, { useState } from 'react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-center border border-input rounded-lg bg-background focus-within:ring-2 focus-within:ring-primary focus-within:border-primary/50">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Message AI Task Assistant..."
          disabled={disabled}
          className="flex-1 bg-transparent border-none focus:outline-none focus:ring-0 py-3 px-4 text-foreground placeholder-muted-foreground disabled:opacity-50"
          aria-label="Type your message"
        />
        <button
          type="submit"
          disabled={disabled || !inputValue.trim()}
          className="mr-3 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Send message"
        >
          Send
        </button>
      </div>
      <div className="mt-2 text-xs text-muted-foreground text-center">
        AI Task Assistant can help you manage your tasks using natural language
      </div>
    </form>
  );
};

export default ChatInput;