# backend/apps/logic_builder/admin.py

from django.contrib import admin
from .models import LogicRule

@admin.register(LogicRule)
class LogicRuleAdmin(admin.ModelAdmin):
    list_display = ('template', 'created_at')
    search_fields = ('template__name',)
