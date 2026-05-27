from pypdf import PdfReader

def extract_resume_text(file_path: str) -> str:
    """Extract text from uploaded PDF resume."""
    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text).strip()
