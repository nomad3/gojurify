from rest_framework import serializers
from documents.models import DocumentTemplate
from users.models import CustomUser

class DocumentTemplateSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = DocumentTemplate
        fields = ['id', 'name', 'content', 'fields', 'owners']
