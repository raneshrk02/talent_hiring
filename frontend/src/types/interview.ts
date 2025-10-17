export interface CandidateInfo {
  fullName: string;
  email: string;
  phone: string;
  yearsExperience: string;
  desiredPosition: string;
  location: string;
  techStack: string[];
  technicalAnswers: Record<string, string>;
  timestamp: string;
}

export interface Message {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: Date;
}

export type ConversationStage = 
  | 'greeting'
  | 'name'
  | 'email'
  | 'phone'
  | 'experience'
  | 'position'
  | 'location'
  | 'techStack'
  | 'technicalQuestions'
  | 'complete';
