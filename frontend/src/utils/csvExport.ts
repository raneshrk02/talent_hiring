import { CandidateInfo } from '@/types/interview';

export const exportToCSV = (candidateInfo: CandidateInfo) => {
  const headers = [
    'Timestamp',
    'Full Name',
    'Email',
    'Phone',
    'Years of Experience',
    'Desired Position',
    'Location',
    'Tech Stack',
    'Technical Questions & Answers'
  ];

  // Support both new (technicalQA) and legacy (technicalAnswers) formats
  let techAnswers = '';
  if (candidateInfo.technicalQA && candidateInfo.technicalQA.length > 0) {
    techAnswers = candidateInfo.technicalQA
      .map((qa, idx) => `Q${idx + 1}: ${qa.question}\nA${idx + 1}: ${qa.answer}`)
      .join('\n\n');
  } else {
    techAnswers = Object.entries(candidateInfo.technicalAnswers)
      .map(([q, a]) => `Q: ${q}\nA: ${a}`)
      .join('\n\n');
  }

  const row = [
    candidateInfo.timestamp,
    candidateInfo.fullName,
    candidateInfo.email,
    candidateInfo.phone,
    candidateInfo.yearsExperience,
    candidateInfo.desiredPosition,
    candidateInfo.location,
    candidateInfo.techStack.join('; '),
    `"${techAnswers}"`
  ];

  const csvContent = [
    headers.join(','),
    row.map(field => {
      const strField = String(field);
      return strField.includes(',') ? `"${strField}"` : strField;
    }).join(',')
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `candidate_${candidateInfo.fullName.replace(/\s+/g, '_')}_${Date.now()}.csv`);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Note: Saving is now handled by the backend via API
// This function is kept for backward compatibility but should not be used
export const saveToLocalStorage = (candidateInfo: CandidateInfo) => {
  console.warn('saveToLocalStorage is deprecated. Data is now saved via backend API.');
};
