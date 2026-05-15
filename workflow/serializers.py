from rest_framework import serializers
from .models import LegalDocument, DraftOutput, OperatorEdit


class LegalDocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = ["id", "file", "original_name", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]


class DraftOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftOutput
        fields = ["id", "document", "task_type", "draft", "evidence", "created_at"]


class OperatorEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorEdit
        fields = ["id", "draft", "edited_text", "learned_rules", "created_at"]
        read_only_fields = ["id", "learned_rules", "created_at"]