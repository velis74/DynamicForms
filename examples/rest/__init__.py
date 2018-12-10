from rest_framework import routers

from examples.rest.filter import FilterViewSet
from .hidden_fields import HiddenFieldsViewSet
from .basic_fields import BasicFieldsViewset
from .advanced_fields import AdvancedFieldsViewset
from .validated import ValidatedViewSet
from .page_load import PageLoadViewSet


router = routers.DefaultRouter()
router.register(r'hidden-fields', HiddenFieldsViewSet, base_name='hidden-fields')
router.register(r'basic-fields', BasicFieldsViewset, base_name='basic-fields')
router.register(r'advanced-fields', AdvancedFieldsViewset, base_name='advanced-fields')
router.register(r'validated', ValidatedViewSet, base_name='validated')
router.register(r'page-load', PageLoadViewSet, base_name='page-load')
router.register(r'filter', FilterViewSet, base_name='filter')
