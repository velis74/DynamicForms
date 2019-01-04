from dynamicforms import fields, serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import Relation


class RelationSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Relation fields list',
        'new': 'New relation object',
        'edit': 'Editing relation object',
    }

    name = fields.CharField()

    class Meta:
        model = Relation
        exclude = ()


class RelationViewset(ModelViewSet):
    template_context = dict(url_reverse='relation')
    pagination_class = viewsets.ModelViewSet.generate_paged_loader(30)

    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
