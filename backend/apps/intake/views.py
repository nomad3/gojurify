from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from documents.models import DocumentTemplate
from django.http import HttpResponse
from django.template import Template, Context
from .utils import generate_document

@login_required
def intake_form(request, template_id):
    template = get_object_or_404(DocumentTemplate, pk=template_id)
    if request.method == 'POST':
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        document_content = generate_document(template, data)
        response = HttpResponse(document_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="document.pdf"'
        return response
    else:
        fields = template.fields
        return render(request, 'intake/intake_form.html', {'fields': fields, 'template': template})
