from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DocumentTemplate
from .forms import DocumentTemplateForm
from django.http import HttpResponseForbidden

@login_required
def template_list(request):
    templates = DocumentTemplate.objects.filter(owners=request.user)
    return render(request, 'documents/template_list.html', {'templates': templates})

@login_required
def template_create(request):
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST)
        if form.is_valid():
            template = form.save()
            template.owners.add(request.user)
            return redirect('documents:template_list')
    else:
        form = DocumentTemplateForm()
    return render(request, 'documents/template_form.html', {'form': form})

@login_required
def template_edit(request, pk):
    template = get_object_or_404(DocumentTemplate, pk=pk)
    if request.user not in template.owners.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('documents:template_list')
    else:
        form = DocumentTemplateForm(instance=template)
    return render(request, 'documents/template_form.html', {'form': form})

@login_required
def invite_collaborator(request, template_id):
    template = get_object_or_404(DocumentTemplate, pk=template_id)
    if request.user not in template.owners.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            template.owners.add(user)
            # Optional: Notify user via email
            return redirect('documents:template_detail', pk=template_id)
    return render(request, 'documents/invite_collaborator.html', {'template': template})
