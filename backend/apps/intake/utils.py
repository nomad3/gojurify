from django.template import Template, Context
from logic_builder.models import LogicRule

def generate_document(template, context_data):
    latest_template = DocumentTemplate.objects.filter(id=template.id).order_by('-version').first()
    context_data = apply_logic(latest_template, context_data)
    django_template = Template(latest_template.content)
    context = Context(context_data)
    rendered_content = django_template.render(context)
    return rendered_content
def apply_logic(template, context_data):
    logic_rules = LogicRule.objects.filter(template=template, version=template.version)
    for rule in logic_rules:
        if evaluate_condition(rule.condition, context_data):
            context_data = perform_action(rule.action, context_data)
    return context_data

def evaluate_condition(condition, context_data):
    # Implement your condition evaluation logic
    pass

def perform_action(action, context_data):
    # Implement your action execution logic
    pass
