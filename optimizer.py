import os
from openai import OpenAI

def generate_ai_suggestions(resume_text: str, jd_text: str, match_data: dict, context_chunks: list):
    """
    If OPENAI_API_KEY is available, the app generates LLM suggestions.
    If not, the app still works with fallback recommendations.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return fallback_suggestions(match_data)

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an expert ATS resume optimizer and technical recruiter.

Analyze this resume against the job description.

Return output in this exact structure:
1. Resume Summary Improvement
2. Top Missing Keywords
3. Improved Resume Bullets
4. Final Recommendations

ATS score: {match_data.get("ats_score")}
Matched skills: {match_data.get("matched_skills")}
Missing skills: {match_data.get("missing_skills")}

Retrieved context:
{context_chunks}

Resume:
{resume_text[:5000]}

Job Description:
{jd_text[:5000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional ATS resume optimization assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

def fallback_suggestions(match_data: dict):
    missing = match_data.get("missing_skills", [])
    matched = match_data.get("matched_skills", [])

    return {
        "summary_improvement": "Write a concise 3-line summary focused on the target role, technical strengths, and measurable results.",
        "matched_keywords": matched,
        "missing_keywords": missing,
        "improved_bullets": [
            "Strengthen resume bullets by adding measurable impact, tools used, and business outcome.",
            "Add role-specific keywords naturally into Skills, Projects, and Experience sections.",
            "Rewrite project descriptions to show ownership, technical depth, deployment, and evaluation results."
        ],
        "final_recommendations": [
            "Use action verbs and metrics in every experience bullet.",
            "Group skills by category: Languages, ML/AI, Data, Cloud, and Tools.",
            "Tailor the resume separately for each job description."
        ]
    }
