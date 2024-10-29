from django.db import models
from django.core.exceptions import ValidationError
from documents.models import DocumentTemplate
import jsonschema

class LogicRule(models.Model):
    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name='logic_rules'
    )
    condition = models.JSONField()
    action = models.JSONField()
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # JSON schemas for validation
    CONDITION_SCHEMA = {
        "type": "object",
        "properties": {
            "field": {"type": "string"},
            "operator": {"type": "string", "enum": ["equals", "not_equals", "greater_than", "less_than"]},
            "value": {"type": ["string", "number", "boolean"]}
        },
        "required": ["field", "operator", "value"]
    }

    ACTION_SCHEMA = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ["show", "hide", "require", "calculate"]},
            "target": {"type": "string"},
            "value": {"type": ["string", "number", "boolean", "null"]}
        },
        "required": ["type", "target"]
    }

    class Meta:
        ordering = ['-created_at', 'version']
        constraints = [
            models.UniqueConstraint(
                fields=['template', 'version'],
                name='unique_rule_version'
            )
        ]

    def clean(self):
        try:
            jsonschema.validate(instance=self.condition, schema=self.CONDITION_SCHEMA)
            jsonschema.validate(instance=self.action, schema=self.ACTION_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(f"Invalid JSON format: {str(e)}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def evaluate_condition(self, context_data):
        """
        Evaluates the condition against provided context data.
        """
        try:
            field_value = context_data.get(self.condition['field'])
            operator = self.condition['operator']
            compare_value = self.condition['value']

            if operator == 'equals':
                return field_value == compare_value
            elif operator == 'not_equals':
                return field_value != compare_value
            elif operator == 'greater_than':
                return float(field_value) > float(compare_value)
            elif operator == 'less_than':
                return float(field_value) < float(compare_value)
            return False
        except (KeyError, ValueError, TypeError) as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error evaluating condition: {str(e)}")
            return False

    def apply_action(self, context_data):
        """
        Applies the action to the context data.
        """
        try:
            action_type = self.action['type']
            target = self.action['target']
            value = self.action.get('value')

            if action_type == 'show':
                context_data[f'{target}_visible'] = True
            elif action_type == 'hide':
                context_data[f'{target}_visible'] = False
            elif action_type == 'require':
                context_data[f'{target}_required'] = True
            elif action_type == 'calculate':
                if value and isinstance(value, str):
                    # Safe evaluation of mathematical expressions
                    from asteval import Interpreter
                    aeval = Interpreter()
                    result = aeval(value)
                    context_data[target] = result

            return context_data
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error applying action: {str(e)}")
            return context_data

    def __str__(self):
        return f"LogicRule for {self.template.name} (v{self.version})"