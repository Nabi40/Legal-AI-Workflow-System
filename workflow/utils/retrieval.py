import numpy as np
from workflow.models import DocumentChunk
from .embeddings import embed_text


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve_relevant_chunks(document, query, top_k=5):
    query_embedding = embed_text(query)
    chunks = DocumentChunk.objects.filter(document=document)

    scored = []

    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk.embedding)
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    evidence = []

    for score, chunk in scored[:top_k]:
        evidence.append({
            "chunk_id": chunk.id,
            "score": round(score, 4),
            "source": document.original_name,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
        })

    return evidence