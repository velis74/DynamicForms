from dynamicforms import fields, serializers
from dynamicforms.viewsets import ModelViewSet

from ..models import Document


class DocumentsSerializer(serializers.ModelSerializer):
    template_context = dict(url_reverse="documents")
    form_titles = {
        "table": "Document list",
        "new": "New document object",
        "edit": "Editing document object",
    }

    file = fields.FileField(allow_empty_file=False, use_url=False, allow_null=True)

    class Meta:
        model = Document
        exclude = ()


class DocumentsViewset(ModelViewSet):
    pagination_class = ModelViewSet.generate_paged_loader(30)

    queryset = Document.objects.all()
    serializer_class = DocumentsSerializer
