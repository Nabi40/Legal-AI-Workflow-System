from django.urls import path
from .views import (
    DocumentUploadAPIView,
    GenerateDraftAPIView,
    OperatorEditAPIView,
)

urlpatterns = [
    path("upload/", DocumentUploadAPIView.as_view()),
    path("generate-draft/", GenerateDraftAPIView.as_view()),
    path("operator-edit/", OperatorEditAPIView.as_view()),
]