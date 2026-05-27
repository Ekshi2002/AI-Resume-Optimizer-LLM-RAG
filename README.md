# AI Resume Optimizer using LLM + RAG

A modern AI-powered resume optimization web app that analyzes a resume against a job description and returns an ATS-style match score, matched skills, missing skills, RAG-based context retrieval, and AI-generated improvement suggestions.

## Features

- Resume PDF upload
- Job description input
- ATS-style similarity score
- Matched skill detection
- Missing skill detection
- Lightweight RAG retrieval using FAISS
- OpenAI-powered resume improvement suggestions
- Dark modern SaaS-style React interface
- Flask backend API

## Tech Stack

### Frontend
- React
- Vite
- CSS
- Lucide React icons

### Backend
- Flask
- Python
- PyPDF
- Scikit-learn
- FAISS
- OpenAI API

## Project Structure

```text
AI-Resume-Optimizer-LLM-RAG/
├── backend/
│   ├── app.py
│   ├── resume_parser.py
│   ├── scoring.py
│   ├── rag_engine.py
│   ├── optimizer.py
│   ├── requirements.txt
│   ├── .env.example
│   └── uploads/
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       └── style.css
│
└── README.md
```

## How to Run

### 1. Backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```bash
copy .env.example .env
```

Add your OpenAI API key inside `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run backend:

```bash
python app.py
```

Backend runs at:

```text
http://localhost:5000
```

### 2. Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## How It Works

1. User uploads resume PDF.
2. User pastes job description.
3. Backend extracts resume text.
4. App compares resume and JD using TF-IDF similarity.
5. Skill matcher detects matched and missing keywords.
6. FAISS retrieves relevant resume/JD chunks.
7. OpenAI generates resume improvement suggestions.
8. React dashboard displays results.

## Resume Bullet

Developed a full-stack AI Resume Optimizer using Flask, React, OpenAI API, and FAISS-based RAG to evaluate resume–job description alignment, compute ATS-style match scores, identify missing skills, and generate targeted resume improvement suggestions.
