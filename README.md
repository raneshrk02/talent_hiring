# Talent Hiring Platform

A modern, full-stack platform for technology recruitment, featuring an AI-powered interview chatbot, candidate info extraction, and recruiter tools.

## Demo
🎥 [Watch the demonstration on YouTube](https://www.youtube.com/watch?v=TWSXg00sbnw)

## Features
- **AI Interview Chatbot**: FastAPI backend with Groq-hosted LLMs for dynamic candidate screening and technical Q&A.
- **Candidate Info Extraction**: Robust parsing of candidate details (name, email, phone, experience, tech stack, etc.).
- **Technical Question Generation**: Automated, skill-specific technical questions for each candidate.
- **MongoDB Storage**: Candidate data is securely stored and managed.
- **Frontend Dashboard**: React + Vite UI for recruiters to view candidate summaries, export CSVs, and manage interviews.
- **CSV Export**: Download candidate data for review and reporting.

## Tech Stack
- **Backend**: Python, FastAPI, MongoDB, Groq LLM API
- **Frontend**: React, TypeScript, Vite, Tailwind CSS


## File Structure
```
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── mongodb.py
│   │   ├── routes/
│   │   ├── schemas.py
│   │   ├── services/
│   │   ├── system_prompt.py
│   │   ├── utils/
│   │   └── __init__.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── data/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── types/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── README.md
├── .gitignore
└── README.md
```

## Getting Started
### Clone the Repository
```sh
git clone https://github.com/raneshrk02/talent_hiring.git
cd talent_hiring
```

### Backend Setup
```sh
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```sh
cd frontend
npm i
npm run build
npm run dev
```

## Configuration
- Backend: Create `backend/.env` with at least:
	- `DATABASE_URL` for MongoDB (e.g., `mongodb://localhost:27017`)
		- `GROQ_API` (required) and optional `GROQ_MODEL` (default `llama-3.1-8b-instant`)
- Frontend: Configure API endpoints in `src/api/endpoints.ts`.