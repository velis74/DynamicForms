from rest_framework import routers

from examples.rest.filter import FilterViewSet
from .advanced_fields import AdvancedFieldsViewset
from .basic_fields import BasicFieldsViewset
from .hidden_fields import HiddenFieldsViewSet
from .page_load import PageLoadViewSet
from .refresh_types import RefreshTypesViewSet
from .relation import RelationViewset
from .single_dialog import SingleDialogViewSet
from .validated import ValidatedViewSet

router = routers.DefaultRouter()
router.register(r'hidden-fields', HiddenFieldsViewSet, base_name='hidden-fields')
router.register(r'basic-fields', BasicFieldsViewset, base_name='basic-fields')
router.register(r'advanced-fields', AdvancedFieldsViewset, base_name='advanced-fields')
router.register(r'relation', RelationViewset, base_name='relation')
router.register(r'validated', ValidatedViewSet, base_name='validated')
router.register(r'page-load', PageLoadViewSet, base_name='page-load')
router.register(r'filter', FilterViewSet, base_name='filter')
router.register(r'refresh-types', RefreshTypesViewSet, base_name='refresh-types')
router.register(r'single-dialog', SingleDialogViewSet, base_name='single-dialog')
