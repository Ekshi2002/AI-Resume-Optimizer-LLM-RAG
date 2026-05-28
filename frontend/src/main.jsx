import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { Upload, Sparkles, Target, CheckCircle, AlertCircle } from "lucide-react";
import "./style.css";

function App() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const analyzeResume = async () => {
    setError("");
    setResult(null);

    if (!resume || !jd.trim()) {
      setError("Please upload a resume PDF and paste a job description.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jd);

    try {
      setLoading(true);

      const response = await fetch("https://ai-resume-optimizer-llm-rag.onrender.com/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong.");
      } else {
        setResult(data);
      }
    } catch {
      setError("Backend is not running. Start Flask on port 5000.");
    } finally {
      setLoading(false);
    }
  };

  const match = result?.match_data;

  return (
    <div className="page">
      <section className="hero">
        <div className="badge">
          <Sparkles size={16} />
          LLM + RAG Resume Intelligence
        </div>

        <h1>AI Resume Optimizer</h1>
        <p>
          Upload your resume, paste a job description, and get an ATS-style score,
          missing skills, matched keywords, and AI-powered improvement suggestions.
        </p>
      </section>

      <main className="card">
        <div className="grid">
          <div className="panel">
            <h2><Upload size={20} /> Upload Resume</h2>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setResume(e.target.files[0])}
            />
            {resume && <p className="small">Selected: {resume.name}</p>}
          </div>

          <div className="panel">
            <h2><Target size={20} /> Job Description</h2>
            <textarea
              placeholder="Paste the job description here..."
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />
          </div>
        </div>

        {error && (
          <div className="error">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        <button onClick={analyzeResume} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </main>

      {match && (
        <section className="results">
          <div className="score-card">
            <div className="score">{match.ats_score}%</div>
            <p>ATS Match Score</p>
          </div>

          <div className="result-grid">
            <div className="result-box">
              <h3><CheckCircle size={18} /> Matched Skills</h3>
              <div className="chips">
                {match.matched_skills.length ? match.matched_skills.map((skill) => (
                  <span className="chip success" key={skill}>{skill}</span>
                )) : <p>No matched skills found.</p>}
              </div>
            </div>

            <div className="result-box">
              <h3><AlertCircle size={18} /> Missing Skills</h3>
              <div className="chips">
                {match.missing_skills.length ? match.missing_skills.map((skill) => (
                  <span className="chip warning" key={skill}>{skill}</span>
                )) : <p>No major missing skills found.</p>}
              </div>
            </div>
          </div>

          <div className="result-box full">
            <h3>AI Recommendations</h3>
            <pre>{typeof result.ai_suggestions === "string"
              ? result.ai_suggestions
              : JSON.stringify(result.ai_suggestions, null, 2)}
            </pre>
          </div>
        </section>
      )}
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
