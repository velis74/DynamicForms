from rest_framework import routers

from examples.rest.filter import FilterViewSet
from .advanced_fields import AdvancedFieldsViewset
from .basic_fields import BasicFieldsViewset
from .calculated_css_class_for_table_row import CalculatedCssClassForTableRowViewSet
from .choice_allow_tags_fields import ChoiceAllowTagsFieldsViewSet
from .document import DocumentsViewset
from .hidden_fields import HiddenFieldsViewSet
from .page_load import PageLoadViewSet
from .refresh_types import RefreshTypesViewSet
from .relation import RelationViewset
from .single_dialog import SingleDialogViewSet
from .validated import ValidatedViewSet
from .write_only_fields import WriteOnlyFieldsViewSet

router = routers.DefaultRouter()
router.register(r'hidden-fields', HiddenFieldsViewSet, 'hidden-fields')
router.register(r'basic-fields', BasicFieldsViewset, 'basic-fields')
router.register(r'advanced-fields', AdvancedFieldsViewset, 'advanced-fields')
router.register(r'relation', RelationViewset, 'relation')
router.register(r'validated', ValidatedViewSet, 'validated')
router.register(r'page-load', PageLoadViewSet, 'page-load')
router.register(r'filter', FilterViewSet, 'filter')
router.register(r'refresh-types', RefreshTypesViewSet, 'refresh-types')
router.register(r'single-dialog', SingleDialogViewSet, 'single-dialog')
router.register(r'write-only-fields', WriteOnlyFieldsViewSet, 'write-only-fields')
router.register(r'choice-allow-tags-fields', ChoiceAllowTagsFieldsViewSet, 'choice-allow-tags-fields')
router.register(r'calculated-css-class-for-table-row', CalculatedCssClassForTableRowViewSet,
                'calculated-css-class-for-table-row')
router.register(r'documents', DocumentsViewset, 'documents')
