from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from documents.models import DocumentTemplate
from django.http import HttpResponse
from django.template import Template, Context
from .utils import generate_document

@login_required
from django.http import Http404

def intake_form(request, template_id):
    template = DocumentTemplate.objects.filter(pk=template_id).order_by('-version').first()
    if not template:
        raise Http404("Template not found")
    if request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        document_content = generate_document(template, data)
        response = HttpResponse(document_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="document_v{template.version}.pdf"'
        return response
    else:
        fields = template.fields
        return render(request, 'intake/intake_form.html', {'fields': fields, 'template': template})
