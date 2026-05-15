from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LegalDocument, DraftOutput
from .serializers import (
    LegalDocumentUploadSerializer,
    DraftOutputSerializer,
    OperatorEditSerializer,
)
from .utils.pipeline import LegalDocumentPipeline


pipeline = LegalDocumentPipeline()


class DocumentUploadAPIView(APIView):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file uploaded. Use form-data key: file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        document = LegalDocument.objects.create(
            file=file,
            original_name=file.name,
            status="uploaded"
        )

        try:
            pipeline.process_document(document)
        except Exception as e:
            document.status = "failed"
            document.save()

            return Response(
                {
                    "error": "Document processing failed.",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = LegalDocumentUploadSerializer(document)

        return Response(
            {
                "message": "Document uploaded and processed successfully.",
                "document": serializer.data,
                "structured_data": document.structured_data,
                "extracted_text_preview": document.extracted_text[:1000],
            },
            status=status.HTTP_201_CREATED
        )


class GenerateDraftAPIView(APIView):
    def post(self, request):
        document_id = request.data.get("document_id")
        task_type = request.data.get("task_type", "case_fact_summary")

        if not document_id:
            return Response(
                {"error": "document_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            document = LegalDocument.objects.get(id=document_id)
        except LegalDocument.DoesNotExist:
            return Response(
                {"error": "Document not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        draft_text, evidence = pipeline.generate_draft(
            document=document,
            task_type=task_type
        )

        draft = DraftOutput.objects.create(
            document=document,
            task_type=task_type,
            draft=draft_text,
            evidence=evidence
        )

        serializer = DraftOutputSerializer(draft)

        return Response(
            {
                "message": "Grounded draft generated successfully.",
                "result": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )


class OperatorEditAPIView(APIView):
    def post(self, request):
        serializer = OperatorEditSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        draft_id = request.data.get("draft")
        edited_text = request.data.get("edited_text")

        try:
            draft = DraftOutput.objects.get(id=draft_id)
        except DraftOutput.DoesNotExist:
            return Response(
                {"error": "Draft not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        learned_rules = pipeline.learn_from_edit(
            original_text=draft.draft,
            edited_text=edited_text
        )

        edit = serializer.save(learned_rules=learned_rules)

        return Response(
            {
                "message": "Operator edit saved and reusable rules learned.",
                "edit": OperatorEditSerializer(edit).data,
                "learned_rules": learned_rules,
            },
            status=status.HTTP_201_CREATED
        )