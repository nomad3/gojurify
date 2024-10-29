from rest_framework import serializers
from documents.models import DocumentTemplate, DocumentTemplateOwnership
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.db import transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DocumentTemplateOwnershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DocumentTemplateOwnership
        fields = ['user', 'access_level', 'created_at']

class DocumentTemplateSerializer(serializers.ModelSerializer):
    owners = DocumentTemplateOwnershipSerializer(
        source='documenttemplateownership_set',
        many=True,
        read_only=True
    )
    export_urls = serializers.SerializerMethodField()
    current_user_access = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentTemplate
        fields = [
            'id', 'name', 'content', 'fields',
            'version', 'created_at', 'updated_at',
            'owners', 'export_urls', 'current_user_access'
        ]
        read_only_fields = ['version', 'created_at', 'updated_at']
        
    def get_export_urls(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
            
        return {
            'pdf': reverse(
                'api:document-template-export-pdf',
                args=[obj.id],
                request=request
            ),
            'word': reverse(
                'api:document-template-export-word',
                args=[obj.id],
                request=request
            ),
            'google_docs': reverse(
                'api:document-template-export-google-docs',
                args=[obj.id],
                request=request
            )
        }
        
    def get_current_user_access(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                ownership = DocumentTemplateOwnership.objects.get(
                    template=obj,
                    user=request.user
                )
                return ownership.access_level
            except DocumentTemplateOwnership.DoesNotExist:
                return None
        return None
        
    def validate_fields(self, value):
        """Validate the fields JSON data."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Fields must be a list")
            
        for field in value:
            if not isinstance(field, dict):
                raise serializers.ValidationError("Each field must be an object")
            if 'name' not in field:
                raise serializers.ValidationError("Each field must have a name")
            if 'type' not in field:
                raise serializers.ValidationError("Each field must have a type")
                
        return value
        
    def create(self, validated_data):
        user = self.context['request'].user
        with transaction.atomic():
            template = super().create(validated_data)
            DocumentTemplateOwnership.objects.create(
                template=template,
                user=user,
                access_level='admin'
            )
        return template
