from rest_framework import routers

from examples.rest.filter import FilterViewSet

from .actions_overview import ActionsOverviewViewSet
from .advanced_fields import AdvancedFieldsViewset
from .basic_fields import BasicFieldsViewset
from .calculated_css_class_for_table_row import CalculatedCssClassForTableRowViewSet
from .calendar import CalendarEventViewSet
from .calendar_reminders import CalendarRemindersViewSet
from .choice_allow_tags_fields import ChoiceAllowTagsFieldsViewSet
from .document import DocumentsViewset
from .hidden_fields import HiddenFieldsViewSet
from .page_load import PageLoadViewSet
from .relation import RelationViewset
from .single_dialog import SingleDialogViewSet
from .validated import ValidatedViewSet
from .write_only_fields import WriteOnlyFieldsViewSet

router = routers.DefaultRouter()
router.register(r"hidden-fields", HiddenFieldsViewSet, "hidden-fields")
router.register(r"actions-overview", ActionsOverviewViewSet, "actions-overview")
router.register(r"basic-fields", BasicFieldsViewset, "basic-fields")
router.register(r"advanced-fields", AdvancedFieldsViewset, "advanced-fields")
router.register(r"relation", RelationViewset, "relation")
router.register(r"validated", ValidatedViewSet, "validated")
router.register(r"page-load", PageLoadViewSet, "page-load")
router.register(r"filter", FilterViewSet, "filter")
router.register(r"single-dialog", SingleDialogViewSet, "single-dialog")
router.register(r"write-only-fields", WriteOnlyFieldsViewSet, "write-only-fields")
router.register(r"choice-allow-tags-fields", ChoiceAllowTagsFieldsViewSet, "choice-allow-tags-fields")
router.register(
    r"calculated-css-class-for-table-row", CalculatedCssClassForTableRowViewSet, "calculated-css-class-for-table-row"
)
router.register(r"documents", DocumentsViewset, "documents")
router.register(r"calendar-event", CalendarEventViewSet, "calendar-event")
router.register(r"calendar-reminder", CalendarRemindersViewSet, "calendar-reminder")
