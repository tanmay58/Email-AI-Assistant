"""""

# backend/app/services/rag_service.py
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import List, Tuple

KB_DIR = os.path.join("app", "kb")

class SimpleRAG:
    def __init__(self):
        self.docs: List[str] = []
        self.meta: List[dict] = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._load_kb()

    def _load_kb(self):
        files = []
        if os.path.exists(KB_DIR):
            for fname in os.listdir(KB_DIR):
                path = os.path.join(KB_DIR, fname)
                if os.path.isfile(path) and fname.lower().endswith((".txt", ".md")):
                    files.append((fname, path))
        for fname, path in files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
            except Exception:
                continue
            if not text:
                continue
            self.docs.append(text)
            self.meta.append({"filename": fname})
        if self.docs:
            self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.docs)

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, dict]]:
        if not self.docs or self.tfidf_matrix is None:
            return []
        q_vec = self.vectorizer.transform([query])
        cosine_similarities = linear_kernel(q_vec, self.tfidf_matrix).flatten()
        top_indices = cosine_similarities.argsort()[::-1][:top_k]
        results = []
        for idx in top_indices:
            results.append((self.docs[idx], self.meta[idx]))
        return results

# singleton
RAG = SimpleRAG()

def retrieve_contexts(query: str, top_k: int = 3):
    
    Returns a list of dicts: [{"text": "...", "meta": {"filename": "..."}}...]
    
    results = RAG.retrieve(query, top_k=top_k)
    contexts = []
    for text, meta in results:
        snippet = text.strip()
        # truncate long docs so prompts aren't huge
        if len(snippet) > 1000:
            snippet = snippet[:1000] + "..."
        contexts.append({"text": snippet, "meta": meta})
    return contexts
"""

# app/services/rag_service.py
from app.utils.db import kb_collection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import threading

class MongoTFIDFRetriever:
    def __init__(self):
        self.lock = threading.Lock()
        self._docs = []
        self._meta = []
        self._vectorizer = None
        self._matrix = None
        self._loaded = False
        self._load()

    def _load(self):
        docs = list(kb_collection.find({}))
        texts = []
        metas = []
        for d in docs:
            t = d.get("text", "") or d.get("content", "")
            if not t or len(t.strip()) < 50:
                continue
            texts.append(t)
            metas.append({"id": str(d.get("_id")), "filename": d.get("filename", "")})
        if texts:
            vec = TfidfVectorizer(stop_words="english", max_features=5000)
            mat = vec.fit_transform(texts)
            with self.lock:
                self._docs = texts
                self._meta = metas
                self._vectorizer = vec
                self._matrix = mat
                self._loaded = True
        else:
            with self.lock:
                self._docs = []
                self._meta = []
                self._vectorizer = None
                self._matrix = None
                self._loaded = True

    def refresh(self):
        self._load()

    def retrieve(self, query: str, top_k: int = 3):
        if not self._loaded:
            self._load()
        with self.lock:
            if not self._docs or self._matrix is None or self._vectorizer is None:
                return []
            qv = self._vectorizer.transform([query])
            sims = linear_kernel(qv, self._matrix).flatten()
            idxs = sims.argsort()[::-1][:top_k]
            results = []
            for i in idxs:
                results.append({
                    "text": self._docs[i],
                    "meta": self._meta[i],
                    "score": float(sims[i])
                })
            return results

RETRIEVER = MongoTFIDFRetriever()

def retrieve_contexts(query: str, top_k: int = 3):
    return RETRIEVER.retrieve(query, top_k=top_k)
