from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DocumentTemplate(models.Model):
    owners = models.ManyToManyField(User, related_name='document_templates')
    name = models.CharField(max_length=255)
    content = models.TextField()
    fields = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
