import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COMMON_SKILLS = [
    "python", "java", "sql", "javascript", "typescript", "react", "node.js",
    "flask", "django", "fastapi", "aws", "azure", "gcp", "docker", "kubernetes",
    "machine learning", "deep learning", "nlp", "llm", "rag", "langchain",
    "openai", "faiss", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "tableau", "power bi", "snowflake", "databricks", "dbt", "etl", "airflow",
    "git", "github", "ci/cd", "rest api", "linux", "spark", "hadoop",
    "data analysis", "data engineering", "data visualization", "statistics"
]

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_skills(text: str):
    text = clean_text(text)
    found = []

    for skill in COMMON_SKILLS:
        if skill in text:
            found.append(skill.title())

    return sorted(set(found))

def compute_ats_score(resume_text: str, jd_text: str) -> int:
    docs = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(docs)
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return int(round(score * 100))

def analyze_match(resume_text: str, jd_text: str):
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched = sorted(resume_skills.intersection(jd_skills))
    missing = sorted(jd_skills.difference(resume_skills))
    ats_score = compute_ats_score(resume_text, jd_text)

    return {
        "ats_score": ats_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills)
    }
