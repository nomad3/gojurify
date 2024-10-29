# backend/apps/documents/admin.py

from django.contrib import admin
from .models import DocumentTemplate

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('owners',)
    list_filter = ('created_at', 'owners', 'version')
    ordering = ('-created_at', 'version')
    readonly_fields = ('created_at', 'version_history')
    date_hierarchy = 'created_at'
    
    actions = ['export_as_pdf', 'export_as_word', 'export_as_google_docs']

    def export_as_pdf(self, request, queryset):
        for document in queryset:
            # Logic to export document to PDF
            pass
    export_as_pdf.short_description = "Export Selected Documents as PDF"

    def export_as_word(self, request, queryset):
        for document in queryset:
            # Logic to export document to Word
            pass
    export_as_word.short_description = "Export Selected Documents as Word"

    def export_as_google_docs(self, request, queryset):
        for document in queryset:
            # Logic to export document to Google Docs
            pass
    export_as_google_docs.short_description = "Export Selected Documents to Google Docs"

    # Versioning can be handled by a separate model or a versioning library
    # Here is a placeholder for version history display
    def version_history(self, obj):
        return ", ".join([str(version) for version in obj.versions.all()])
    version_history.short_description = "Version History"

