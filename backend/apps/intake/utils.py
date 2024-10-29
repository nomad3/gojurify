from django.template import Template, Context
from logic_builder.models import LogicRule
import operator
import json

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
    """
    Evaluates a logical condition against the provided context data.
    
    condition format:
    {
        "field": "field_name",
        "operator": "equals|not_equals|greater_than|less_than|contains|not_contains",
        "value": "comparison_value"
    }
    """
    try:
        field = condition.get('field')
        op = condition.get('operator')
        value = condition.get('value')
        
        if field not in context_data:
            return False
            
        field_value = context_data[field]
        
        operators = {
            'equals': operator.eq,
            'not_equals': operator.ne,
            'greater_than': operator.gt,
            'less_than': operator.lt,
            'contains': lambda x, y: y in x,
            'not_contains': lambda x, y: y not in x,
            'in': lambda x, y: x in y,
            'not_in': lambda x, y: x not in y
        }
        
        if op not in operators:
            return False
            
        return operators[op](field_value, value)
        
    except Exception as e:
        print(f"Error evaluating condition: {str(e)}")
        return False

def perform_action(action, context_data):
    """
    Performs an action based on the action configuration.
    
    action format:
    {
        "type": "set_value|append|remove|calculate",
        "field": "target_field",
        "value": "new_value"
    }
    """
    try:
        action_type = action.get('type')
        field = action.get('field')
        value = action.get('value')
        
        if action_type == 'set_value':
            context_data[field] = value
            
        elif action_type == 'append':
            if field in context_data:
                context_data[field] += value
            else:
                context_data[field] = value
            
        elif action_type == 'remove':
            if field in context_data:
                del context_data[field]
            
        elif action_type == 'calculate':
            # Implement your calculation logic here
            pass
            
        else:
            raise ValueError(f"Invalid action type: {action_type}")
            
    except Exception as e:
        print(f"Error performing action: {str(e)}")
        raise
