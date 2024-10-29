from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .models import DocumentTemplate, DocumentTemplateOwnership
from .forms import DocumentTemplateForm
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

@login_required
def template_list(request):
    """List templates with pagination and filtering."""
    try:
        templates = DocumentTemplate.objects.filter(
            documenttemplateownership__user=request.user
        ).select_related('owner').distinct()
        
        # Filtering
        search_query = request.GET.get('search')
        if search_query:
            templates = templates.filter(name__icontains=search_query)
            
        # Pagination
        paginator = Paginator(templates, 10)
        page = request.GET.get('page', 1)
        templates = paginator.get_page(page)
        
        return render(request, 'documents/template_list.html', {
            'templates': templates,
            'search_query': search_query
        })
    except Exception as e:
        logger.error(f"Error in template_list: {str(e)}")
        messages.error(request, "An error occurred while loading templates.")
        return render(request, 'documents/template_list.html', {'templates': []})

@login_required
@require_http_methods(["GET", "POST"])
def template_create(request):
    """Create a new document template."""
    try:
        if request.method == 'POST':
            form = DocumentTemplateForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    template = form.save(commit=False)
                    template.save()
                    DocumentTemplateOwnership.objects.create(
                        user=request.user,
                        template=template,
                        access_level='admin'
                    )
                messages.success(request, "Template created successfully.")
                return redirect('documents:template_detail', pk=template.pk)
        else:
            form = DocumentTemplateForm()
        
        return render(request, 'documents/template_form.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in template_create: {str(e)}")
        messages.error(request, "An error occurred while creating the template.")
        return redirect('documents:template_list')

@login_required
@require_http_methods(["GET", "POST"])
def template_edit(request, pk):
    """Edit an existing document template."""
    try:
        template = get_object_or_404(DocumentTemplate, pk=pk)
        ownership = get_object_or_404(
            DocumentTemplateOwnership,
            user=request.user,
            template=template
        )
        
        if ownership.access_level not in ['edit', 'admin']:
            raise PermissionDenied("You don't have permission to edit this template.")
            
        if request.method == 'POST':
            form = DocumentTemplateForm(request.POST, instance=template)
            if form.is_valid():
                with transaction.atomic():
                    template = form.save()
                messages.success(request, "Template updated successfully.")
                return redirect('documents:template_detail', pk=template.pk)
        else:
            form = DocumentTemplateForm(instance=template)
        
        return render(request, 'documents/template_form.html', {
            'form': form,
            'template': template
        })
    except PermissionDenied as e:
        messages.error(request, str(e))
        return redirect('documents:template_list')
    except Exception as e:
        logger.error(f"Error in template_edit: {str(e)}")
        messages.error(request, "An error occurred while editing the template.")
        return redirect('documents:template_list')

@login_required
def template_export(request, pk, format_type):
    """Export template in various formats."""
    try:
        template = get_object_or_404(DocumentTemplate, pk=pk)
        ownership = get_object_or_404(
            DocumentTemplateOwnership,
            user=request.user,
            template=template
        )
        
        if format_type == 'pdf':
            content = template.export_as_pdf()
            content_type = 'application/pdf'
            filename = f"{template.name}.pdf"
        elif format_type == 'word':
            content = template.export_as_word()
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            filename = f"{template.name}.docx"
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
        if content is None:
            messages.error(request, f"Failed to export template as {format_type.upper()}")
            return redirect('documents:template_detail', pk=pk)
            
        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        logger.error(f"Error in template_export: {str(e)}")
        messages.error(request, f"An error occurred while exporting the template as {format_type.upper()}")
        return redirect('documents:template_detail', pk=pk)
