# backend/apps/intake/admin.py

from django.contrib import admin
from .models import IntakeForm  # Assuming you have an IntakeForm model

admin.site.register(IntakeForm)
@admin.register(IntakeForm)
class IntakeFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'version')
    search_fields = ('name',)
    list_filter = ('created_at', 'version')
    ordering = ('-created_at', 'version')
    readonly_fields = ('created_at', 'version')

    actions = ['export_intake_forms_as_csv']

    def export_intake_forms_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="intake_forms.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Created At', 'Version'])

        for form in queryset:
            writer.writerow([form.name, form.created_at, form.version])

        return response
    export_intake_forms_as_csv.short_description = "Export Selected Intake Forms as CSV"
