import { CandidateInfo } from '@/types/interview';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CandidateSummaryProps {
  candidateInfo: CandidateInfo;
}

export const CandidateSummary = ({ candidateInfo }: CandidateSummaryProps) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Candidate Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm font-medium text-muted-foreground">Full Name</p>
            <p className="text-base">{candidateInfo.fullName || '-'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Email</p>
            <p className="text-base break-all">{candidateInfo.email || '-'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Phone</p>
            <p className="text-base">{candidateInfo.phone || '-'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Years of Experience</p>
            <p className="text-base">{candidateInfo.yearsExperience || '-'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Desired Position</p>
            <p className="text-base">{candidateInfo.desiredPosition || '-'}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-muted-foreground">Location</p>
            <p className="text-base">{candidateInfo.location || '-'}</p>
          </div>
        </div>
        
        {candidateInfo.techStack.length > 0 && (
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">Tech Stack</p>
            <div className="flex flex-wrap gap-2">
              {candidateInfo.techStack.map((tech, index) => (
                <Badge key={index} variant="secondary">
                  {tech}
                </Badge>
              ))}
            </div>
          </div>
        )}
        
        {/* Support both new (technicalQA) and legacy (technicalAnswers) formats */}
        {(candidateInfo.technicalQA && candidateInfo.technicalQA.length > 0) && (
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">Technical Q&A</p>
            <div className="space-y-3">
              {candidateInfo.technicalQA.map((qa, index) => (
                <div key={index} className="bg-muted rounded-lg p-3">
                  <p className="text-sm font-medium mb-1">Q: {qa.question}</p>
                  <p className="text-sm text-muted-foreground">A: {qa.answer}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Fallback to legacy format if technicalQA is not available */}
        {(!candidateInfo.technicalQA || candidateInfo.technicalQA.length === 0) && 
         Object.keys(candidateInfo.technicalAnswers).length > 0 && (
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">Technical Q&A</p>
            <div className="space-y-3">
              {Object.entries(candidateInfo.technicalAnswers).map(([question, answer], index) => (
                <div key={index} className="bg-muted rounded-lg p-3">
                  <p className="text-sm font-medium mb-1">Q: {question}</p>
                  <p className="text-sm text-muted-foreground">A: {answer}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
