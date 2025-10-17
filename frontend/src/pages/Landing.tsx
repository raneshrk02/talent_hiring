import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { Bot, Users, CheckCircle, Clock } from 'lucide-react';

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-2">
            <Bot className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">TalentScout</h1>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-16 max-w-5xl">
        <div className="text-center space-y-6 mb-16">
          <h2 className="text-5xl font-bold text-foreground">
            Welcome to TalentScout
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Your AI-powered hiring assistant that conducts intelligent screening interviews, 
            collects candidate information, and generates technical questions based on skills.
          </p>
          <Button 
            size="lg" 
            className="text-lg px-8 py-6 mt-8"
            onClick={() => navigate('/interview')}
          >
            Start Interview
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
          <div className="bg-card border border-border rounded-lg p-6 text-center space-y-3">
            <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
              <Bot className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-semibold text-foreground">AI-Powered</h3>
            <p className="text-sm text-muted-foreground">
              Natural conversation flow with intelligent information extraction
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 text-center space-y-3">
            <div className="w-12 h-12 bg-secondary/10 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle className="w-6 h-6 text-secondary" />
            </div>
            <h3 className="font-semibold text-foreground">Dynamic Questions</h3>
            <p className="text-sm text-muted-foreground">
              Technical questions tailored to candidate's declared tech stack
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 text-center space-y-3">
            <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
              <Clock className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-semibold text-foreground">Time Efficient</h3>
            <p className="text-sm text-muted-foreground">
              Automated screening saves recruiters hours of manual work
            </p>
          </div>

          <div className="bg-card border border-border rounded-lg p-6 text-center space-y-3">
            <div className="w-12 h-12 bg-secondary/10 rounded-full flex items-center justify-center mx-auto">
              <Users className="w-6 h-6 text-secondary" />
            </div>
            <h3 className="font-semibold text-foreground">Data Export</h3>
            <p className="text-sm text-muted-foreground">
              Export candidate data to CSV for easy recruiter review
            </p>
          </div>
        </div>

        <div className="mt-16 bg-card border border-border rounded-lg p-8">
          <h3 className="text-2xl font-bold text-foreground mb-4">How It Works</h3>
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Candidate Information</h4>
                <p className="text-sm text-muted-foreground">
                  Collect basic details through natural conversation: name, email, phone, experience, position, and location
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Tech Stack Discovery</h4>
                <p className="text-sm text-muted-foreground">
                  AI identifies candidate's technical skills including programming languages, frameworks, and tools
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Technical Assessment</h4>
                <p className="text-sm text-muted-foreground">
                  Generate and ask relevant technical questions based on candidate's expertise
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center font-bold">
                4
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Save & Export</h4>
                <p className="text-sm text-muted-foreground">
                  All information is saved and can be exported to CSV for recruiter review
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t border-border bg-card/50 backdrop-blur-sm mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          <p>&copy; 2025 TalentScout. Streamlining the hiring process with AI.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
