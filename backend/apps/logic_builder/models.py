from django.db import models
from documents.models import DocumentTemplate

class LogicRule(models.Model):
    template = models.ForeignKey(DocumentTemplate, on_delete=models.CASCADE, related_name='logic_rules')
    condition = models.JSONField()
    action = models.JSONField()
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LogicRule for {self.template.name} (v{self.version})"