from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from documents.models import DocumentTemplate
from .models import LogicRule
from django.http import HttpResponseForbidden
import json

@login_required
def logic_builder_view(request, template_id):
    template = get_object_or_404(DocumentTemplate, pk=template_id)
    if request.user not in template.owners.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        logic_data = json.loads(request.POST.get('logic_data'))
        LogicRule.objects.create(
            template=template,
            condition=logic_data['condition'],
            action=logic_data['action']
        )
        return redirect('documents:template_edit', pk=template_id)
    return render(request, 'logic_builder/logic_builder.html', {'template': template})
