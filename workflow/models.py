from django.db import models


class LegalDocument(models.Model):
    file = models.FileField(upload_to="legal_docs/")
    original_name = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    structured_data = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50, default="uploaded")
    created_at = models.DateTimeField(auto_now_add=True)


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        LegalDocument,
        on_delete=models.CASCADE,
        related_name="chunks"
    )
    chunk_index = models.IntegerField()
    text = models.TextField()
    embedding = models.JSONField(default=list)
    metadata = models.JSONField(default=dict, blank=True)


class DraftOutput(models.Model):
    document = models.ForeignKey(
        LegalDocument,
        on_delete=models.CASCADE,
        related_name="drafts"
    )
    task_type = models.CharField(max_length=100, default="case_fact_summary")
    draft = models.TextField()
    evidence = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class OperatorEdit(models.Model):
    draft = models.ForeignKey(
        DraftOutput,
        on_delete=models.CASCADE,
        related_name="edits"
    )
    edited_text = models.TextField()
    learned_rules = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class LearnedDraftRule(models.Model):
    rule = models.TextField()
    frequency = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)