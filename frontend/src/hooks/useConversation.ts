import { useState, useCallback, useEffect } from 'react';
import { Message, CandidateInfo, ConversationStage } from '@/types/interview';
import { endpoints, apiClient } from '@/api/endpoints';

const initialCandidateInfo: CandidateInfo = {
  fullName: '',
  email: '',
  phone: '',
  yearsExperience: '',
  desiredPosition: '',
  location: '',
  techStack: [],
  technicalAnswers: {},
  technicalQA: [],
  timestamp: '',
};

export const useConversation = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [stage, setStage] = useState<ConversationStage>('greeting');
  const [candidateInfo, setCandidateInfo] = useState<CandidateInfo>(initialCandidateInfo);
  const [currentTechQuestionIndex, setCurrentTechQuestionIndex] = useState(0);
  const [techQuestionsAsked, setTechQuestionsAsked] = useState<string[]>([]);

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Send message to backend and get AI response
      const response = await apiClient.post<{
        message: string;
        nextStage: ConversationStage;
        updatedCandidateInfo?: Partial<CandidateInfo>;
        technicalQuestion?: string;
        isComplete?: boolean;
      }>(endpoints.sendMessage, {
        userMessage: content,
        currentStage: stage,
        candidateInfo,
        currentTechQuestionIndex,
      });

      // Update candidate info if provided by backend
      if (response.updatedCandidateInfo) {
        setCandidateInfo(prev => ({
          ...prev,
          ...response.updatedCandidateInfo,
        }));
      }

      // Update stage
      setStage(response.nextStage);

      // Handle technical questions
      if (response.technicalQuestion) {
        setTechQuestionsAsked(prev => [...prev, response.technicalQuestion!]);
        setCurrentTechQuestionIndex(prev => prev + 1);
      }

      // Add AI response
      setTimeout(() => {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: response.message,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, aiMessage]);
      }, 500);

  // Candidate data is saved by backend
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, there was an error processing your message. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  }, [stage, candidateInfo, currentTechQuestionIndex]);

  const resetConversation = useCallback(() => {
    setMessages([]);
    setStage('greeting');
    setCandidateInfo(initialCandidateInfo);
    setCurrentTechQuestionIndex(0);
    setTechQuestionsAsked([]);
    
    // Do not add hardcoded greeting; let backend/LLM generate the greeting
    setMessages([]);
  }, []);

  // Initialize conversation on mount and trigger first LLM question
  useEffect(() => {
    resetConversation();
    // Send empty message to backend to get first LLM greeting/question
    sendMessage("");
  }, []);

  return {
    messages,
    stage,
    candidateInfo,
    sendMessage,
    resetConversation
  };
};
