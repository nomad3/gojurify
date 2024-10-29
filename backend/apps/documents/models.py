from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DocumentTemplate(models.Model):
    owners = models.ManyToManyField(User, related_name='document_templates')
    name = models.CharField(max_length=255)
    content = models.TextField()
    fields = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def export_as_pdf(self):
        # Implement PDF export logic
        pass

    def export_as_word(self):
        # Implement Word export logic
        pass

    def export_as_google_docs(self):
        # Implement Google Docs export logic
        pass
