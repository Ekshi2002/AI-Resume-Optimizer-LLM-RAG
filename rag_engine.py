import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

def chunk_text(text: str, chunk_size: int = 120):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks

def retrieve_relevant_context(resume_text: str, jd_text: str, top_k: int = 3):
    """
    Lightweight RAG-style retrieval using TF-IDF vectors + FAISS.
    This gives you retrieval logic without needing paid embeddings for the first version.
    """
    chunks = chunk_text(resume_text) + chunk_text(jd_text)

    if not chunks:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(chunks).toarray().astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    query_vector = vectorizer.transform([jd_text]).toarray().astype("float32")
    distances, indices = index.search(query_vector, min(top_k, len(chunks)))

    return [chunks[i] for i in indices[0]]
