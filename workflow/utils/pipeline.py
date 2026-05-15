from workflow.models import DocumentChunk
from .extraction import extract_text_from_file
from .structuring import extract_structured_data
from .chunking import chunk_text
from .embeddings import embed_text
from .drafting import generate_grounded_draft
from .learning import learn_from_operator_edit


class LegalDocumentPipeline:
    def process_document(self, document):
        extracted_text = extract_text_from_file(document.file.path)
        structured_data = extract_structured_data(extracted_text)

        document.extracted_text = extracted_text
        document.structured_data = structured_data
        document.status = "processed"
        document.save()

        self.create_chunks(document, extracted_text)

        return document

    def create_chunks(self, document, extracted_text):
        DocumentChunk.objects.filter(document=document).delete()

        chunks = chunk_text(extracted_text)

        for index, chunk in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                chunk_index=index,
                text=chunk,
                embedding=embed_text(chunk),
                metadata={
                    "source_file": document.original_name,
                    "chunk_index": index,
                }
            )

    def generate_draft(self, document, task_type="case_fact_summary"):
        return generate_grounded_draft(document, task_type)

    def learn_from_edit(self, original_text, edited_text):
        return learn_from_operator_edit(original_text, edited_text)