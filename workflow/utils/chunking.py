def chunk_text(text, max_words=180, overlap=40):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + max_words
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_words - overlap

    return chunks