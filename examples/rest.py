from rest_framework import routers, serializers, viewsets
from .models import Validated


class ValidatedSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # so that it shows at all

    class Meta:
        model = Validated
        exclude = ()


class ValidatedViewSet(viewsets.ModelViewSet):
    queryset = Validated.objects.all()
    serializer_class = ValidatedSerializer


router = routers.DefaultRouter()
router.register(r'rest/validated', ValidatedViewSet)
