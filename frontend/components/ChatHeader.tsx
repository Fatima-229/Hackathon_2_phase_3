import React from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

interface ChatHeaderProps {
  title: string;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ title }) => {
  return (
    <header className="border-b border-border bg-background sticky top-0 z-10">
      <div className="max-w-4xl w-full mx-auto px-4 py-4 flex items-center">
        <Link href="/dashboard" className="mr-4 text-foreground hover:text-primary transition-colors">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <h1 className="text-xl font-bold text-foreground">{title}</h1>
        <div className="ml-auto flex items-center space-x-2">
          <div className="h-3 w-3 rounded-full bg-green-500"></div>
          <span className="text-sm text-muted-foreground">AI Online</span>
        </div>
      </div>
    </header>
  );
};

export default ChatHeader;