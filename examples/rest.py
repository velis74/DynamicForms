from rest_framework import routers, serializers
from rest_framework.renderers import JSONRenderer

from dynamicforms.renderers import TemplateHTMLRenderer
from dynamicforms.viewsets import ModelViewSet
from .models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # so that it shows at all

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'examples/validated.html'
    list_template_name = 'examples/validated_list.html'
    template_context = dict(crud_form=True)

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer


router = routers.DefaultRouter()
router.register(r'rest/validated', ValidatedViewSet, base_name='validated')
