from rest_framework import routers

from .hidden_fields import HiddenFieldsViewSet
from .validated import ValidatedViewSet
from .page_load import PageLoadViewSet

router = routers.DefaultRouter()
router.register(r'hidden-fields', HiddenFieldsViewSet, base_name='hidden-fields')
router.register(r'validated', ValidatedViewSet, base_name='validated')
router.register(r'page-load', PageLoadViewSet, base_name='page-load')
