import { Message } from '@/types/interview';
import { Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isAssistant = message.role === 'assistant';

  return (
    <div
      className={cn(
        'flex gap-3 mb-4 animate-in fade-in slide-in-from-bottom-2 duration-500',
        isAssistant ? 'justify-start' : 'justify-end'
      )}
    >
      {isAssistant && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          <Bot className="w-5 h-5 text-primary-foreground" />
        </div>
      )}
      
      <div
        className={cn(
          'max-w-[70%] rounded-2xl px-4 py-3 whitespace-pre-wrap',
          isAssistant
            ? 'bg-card text-card-foreground border border-border'
            : 'bg-primary text-primary-foreground'
        )}
      >
        <p className="text-sm leading-relaxed">{message.content}</p>
      </div>
      
      {!isAssistant && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
          <User className="w-5 h-5 text-secondary-foreground" />
        </div>
      )}
    </div>
  );
};
