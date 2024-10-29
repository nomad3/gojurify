# backend/apps/intake/admin.py

from django.contrib import admin
from .models import IntakeForm  # Ensure IntakeForm model exists
from django.http import HttpResponse
import csv

@admin.register(IntakeForm)
class IntakeFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'version')
    search_fields = ('name',)
    list_filter = ('created_at', 'version')
    ordering = ('-created_at', 'version')
    readonly_fields = ('created_at', 'version')

    actions = ['export_intake_forms_as_csv']

    def export_intake_forms_as_csv(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "No intake forms selected for export.", level='warning')
            return
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="intake_forms.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Created At', 'Version'])

        for form in queryset:
            writer.writerow([form.name, form.created_at.strftime("%Y-%m-%d %H:%M"), form.version])

        self.message_user(request, f"Successfully exported {queryset.count()} intake forms.")
        return response
    export_intake_forms_as_csv.short_description = "Export Selected Intake Forms as CSV"
