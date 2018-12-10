from rest_framework import routers

from examples.rest.filter import FilterViewSet
from .hidden_fields import HiddenFieldsViewSet
from .page_load import PageLoadViewSet
from .validated import ValidatedViewSet

router = routers.DefaultRouter()
router.register(r'hidden-fields', HiddenFieldsViewSet, base_name='hidden-fields')
router.register(r'validated', ValidatedViewSet, base_name='validated')
router.register(r'page-load', PageLoadViewSet, base_name='page-load')
router.register(r'filter', FilterViewSet, base_name='filter')
