from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import DocumentTemplateSerializer
from documents.models import DocumentTemplate
from django.http import HttpResponse

class DocumentTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DocumentTemplate.objects.filter(owners=self.request.user)

    @action(detail=True, methods=['get'], url_path='export/pdf')
    def export_pdf(self, request, pk=None):
        template = self.get_object()
        pdf_content = template.export_as_pdf()
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{template.name}.pdf"'
            return response
        return Response({'detail': 'Failed to generate PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='export/word')
    def export_word(self, request, pk=None):
        template = self.get_object()
        word_content = template.export_as_word()
        if word_content:
            response = HttpResponse(word_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{template.name}.docx"'
            return response
        return Response({'detail': 'Failed to generate Word document.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='export/google-docs')
    def export_google_docs(self, request, pk=None):
        template = self.get_object()
        google_docs_url = template.export_as_google_docs()
        if google_docs_url:
            return Response({'google_docs_url': google_docs_url}, status=status.HTTP_200_OK)
        return Response({'detail': 'Failed to export to Google Docs.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
