from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DocumentTemplate
from .forms import DocumentTemplateForm
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

@login_required
def template_list(request):
    templates = DocumentTemplate.objects.filter(owners=request.user).order_by('-created_at', '-version')
    return render(request, 'documents/template_list.html', {'templates': templates})
@login_required
def template_create(request):
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.version = 1
            template.save()
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
    User = get_user_model()
    template = get_object_or_404(DocumentTemplate, pk=template_id)
    if request.user not in template.owners.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            template.owners.add(user)
            subject = "You've been invited to collaborate on a document template"
            message = f"You have been invited by {request.user.username} to collaborate on the document template '{template.name}'."
            from_email = "no-reply@example.com"
            send_mail(subject, message, from_email, [user.email])
            return redirect('documents:template_detail', pk=template_id)
    return render(request, 'documents/invite_collaborator.html', {'template': template})
