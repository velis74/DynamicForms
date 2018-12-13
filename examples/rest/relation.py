from dynamicforms import serializers
from dynamicforms.viewsets import ModelViewSet
from ..models import Relation


class RelationSerializer(serializers.ModelSerializer):
    form_titles = {
        'table': 'Relation fields list',
        'new': 'New relation object',
        'edit': 'Editing relation object',
    }

    name = serializers.CharField()

    class Meta:
        model = Relation
        exclude = ()


class RelationViewset(ModelViewSet):
    template_context = dict(url_reverse='relation')

    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
