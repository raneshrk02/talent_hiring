import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useConversation } from '@/hooks/useConversation';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';
import { CandidateSummary } from '@/components/CandidateSummary';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { exportToCSV, saveToLocalStorage } from '@/utils/csvExport';
import { RefreshCw, Download, ArrowLeft } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const Interview = () => {
  const { messages, stage, candidateInfo, sendMessage, resetConversation } = useConversation();
  const { toast } = useToast();
  const navigate = useNavigate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isComplete = stage === 'complete';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isComplete && candidateInfo.timestamp) {
      saveToLocalStorage(candidateInfo);
      toast({
        title: "Interview Complete",
        description: "Candidate data has been saved successfully.",
      });
    }
  }, [isComplete, candidateInfo, toast]);

  const handleExportCSV = () => {
    exportToCSV(candidateInfo);
    toast({
      title: "CSV Exported",
      description: "Candidate data has been downloaded as CSV.",
    });
  };

  const handleReset = () => {
    window.location.reload();
    setTimeout(() => {
      toast({
        title: "New Interview",
        description: "Ready to start a new interview!",
      });
    }, 500);
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">TalentScout Hiring Assistant</h1>
            <p className="text-sm text-muted-foreground">AI-Powered Initial Screening Interview</p>
          </div>
          <Button variant="outline" onClick={() => navigate('/')}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <Card className="h-[600px] flex flex-col">
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} />
              </div>
              
              <div className="border-t border-border p-4">
                {isComplete ? (
                  <div className="flex gap-2">
                    <Button onClick={handleReset} className="flex-1">
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Start New Interview
                    </Button>
                    <Button onClick={handleExportCSV} variant="secondary">
                      <Download className="w-4 h-4 mr-2" />
                      Export CSV
                    </Button>
                  </div>
                ) : (
                  <ChatInput onSend={sendMessage} />
                )}
              </div>
            </Card>
          </div>

          <div className="lg:col-span-1">
            <CandidateSummary candidateInfo={candidateInfo} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Interview;
