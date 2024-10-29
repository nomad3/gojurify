from rest_framework import serializers
from documents.models import DocumentTemplate
from users.models import CustomUser

from rest_framework.reverse import reverse

class DocumentTemplateSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    export_as_pdf = serializers.SerializerMethodField()
    export_as_word = serializers.SerializerMethodField()
    export_as_google_docs = serializers.SerializerMethodField()

    class Meta:
        model = DocumentTemplate
        fields = ['id', 'name', 'content', 'fields', 'owners', 'export_as_pdf', 'export_as_word', 'export_as_google_docs']

    def get_export_as_pdf(self, obj):
        request = self.context.get('request')
        return reverse('documents:export_as_pdf', args=[obj.id], request=request)

    def get_export_as_word(self, obj):
        request = self.context.get('request')
        return reverse('documents:export_as_word', args=[obj.id], request=request)

    def get_export_as_google_docs(self, obj):
        request = self.context.get('request')
        return reverse('documents:export_as_google_docs', args=[obj.id], request=request)
