import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from resume_parser import extract_resume_text
from scoring import analyze_match
from rag_engine import retrieve_relevant_context
from optimizer import generate_ai_suggestions

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Resume Optimizer API is running"})

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "Resume PDF is required"}), 400

        resume_file = request.files["resume"]
        jd_text = request.form.get("job_description", "")

        if not jd_text.strip():
            return jsonify({"error": "Job description is required"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(file_path)

        resume_text = extract_resume_text(file_path)

        match_data = analyze_match(resume_text, jd_text)
        context_chunks = retrieve_relevant_context(resume_text, jd_text)
        ai_suggestions = generate_ai_suggestions(
            resume_text,
            jd_text,
            match_data,
            context_chunks
        )

        return jsonify({
            "resume_text_preview": resume_text[:800],
            "match_data": match_data,
            "retrieved_context": context_chunks,
            "ai_suggestions": ai_suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
