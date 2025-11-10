// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// API Endpoints
export const endpoints = {
  // Conversation endpoints
  sendMessage: `${API_BASE_URL}/api/conversation/message`,
  getNextQuestion: `${API_BASE_URL}/api/conversation/next-question`,
  
  // Technical questions endpoints
  getTechnicalQuestions: `${API_BASE_URL}/api/technical-questions`,
  getQuestionsByTech: (tech: string) => `${API_BASE_URL}/api/technical-questions/${tech}`,
  
  // Candidate management endpoints
  rejectCandidate: `${API_BASE_URL}/api/candidate/reject`,
  
  // Export endpoints
} as const;

// API Helper functions
export const apiClient = {
  async post<T>(url: string, data: any): Promise<T> {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },

  async get<T>(url: string): Promise<T> {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },

  async put<T>(url: string, data: any): Promise<T> {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },

  async delete<T>(url: string): Promise<T> {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },

  async options(url: string): Promise<void> {
    // Send OPTIONS request for CORS preflight
    await fetch(url, {
      method: 'OPTIONS',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  },
};
