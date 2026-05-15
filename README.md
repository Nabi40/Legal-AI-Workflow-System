## Legal-AI-Workflow-System

An AI-powered Django REST Framework pipeline for processing messy legal-style documents, extracting structured information, retrieving grounded evidence, generating legal-style drafts, and improving future drafts using operator edits.

---
 
## Features (Document Processing)

- Scanned PDFs
- Low-quality PDFs
- Handwritten or partially unclear documents
- Image-based legal files
- Noisy OCR inputs

## Capabilities:

- OCR extraction using Tesseract
- PDF text extraction
- Noise cleanup
- Structured data extraction
- Unclear/low-confidence section detection

##  Grounded Retrieval

- Chunk-based retrieval
- Embedding similarity search
- Evidence ranking
- Inspectable grounding evidence
- Reduced hallucination risk

  
## Draft Generation

- Case fact summaries
- Internal legal memos
- Notice summaries
- Document checklists

----
## Project Structure
```
legal_ai_workflow/
│
├── workflow/
│   ├── migrations/
│   │
│   ├── utils/
│   │   ├── extraction.py
│   │   ├── structuring.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   ├── drafting.py
│   │   ├── learning.py
│   │   └── pipeline.py
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── media/
├── requirements.txt
├── manage.py
└── README.md
```

## System Architecture
```
Upload Document
       │
       ▼
Document Extraction
(PDF/Text/OCR)
       │
       ▼
Text Cleanup
       │
       ▼
Structured Data Extraction
       │
       ▼
Chunking
       │
       ▼
Embedding Generation
       │
       ▼
Retrieval Layer
       │
       ▼
Grounded Draft Generation
       │
       ▼
Operator Review & Edit
       │
       ▼
Learning Loop
```

