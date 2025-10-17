import { CandidateInfo, ConversationStage } from './interview';

// Request types
export interface SendMessageRequest {
  userMessage: string;
  currentStage: ConversationStage;
  candidateInfo: CandidateInfo;
  currentTechQuestionIndex: number;
}

export interface SaveCandidateRequest {
  candidateInfo: CandidateInfo;
}

export interface GetTechnicalQuestionsRequest {
  techStack: string[];
}

// Response types
export interface SendMessageResponse {
  message: string;
  nextStage: ConversationStage;
  updatedCandidateInfo?: Partial<CandidateInfo>;
  technicalQuestion?: string;
  isComplete?: boolean;
}

export interface SaveCandidateResponse {
  id: string;
  message: string;
  success: boolean;
}

export interface TechnicalQuestionsResponse {
  questions: Record<string, string[]>;
}

export interface GetCandidatesResponse {
  candidates: CandidateInfo[];
  total: number;
}

export interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}
