from rest_framework import routers, serializers, viewsets
from rest_framework.renderers import TemplateHTMLRenderer, HTMLFormRenderer
from rest_framework.utils.serializer_helpers import ReturnList

from .models import Validated


class MyTemplateHTMLRenderer(TemplateHTMLRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            data = dict(data=data,
                        serializer=data.serializer.child
                        if isinstance(data.serializer, serializers.ListSerializer) else data.serializer)
        return super().render(data, accepted_media_type, renderer_context)


class ValidatedSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # so that it shows at all

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(viewsets.ModelViewSet):
    renderer_classes = [MyTemplateHTMLRenderer]

    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['examples/validated_list.html']
        return ['examples/validated.html']


router = routers.DefaultRouter()
router.register(r'rest/validated', ValidatedViewSet, base_name='validated')
