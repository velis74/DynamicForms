import threading

from django.conf import settings as s
from django.utils.translation import gettext_lazy as _
from versio.version import Version
from versio.version_scheme import Pep440VersionScheme

from .struct import Struct

DYNAMICFORMS_ROOT = 'dynamicforms/'
DYNAMICFORMS_BOOTSTRAP = DYNAMICFORMS_ROOT + 'bootstrap/'
DYNAMICFORMS_JQUERY_UI = DYNAMICFORMS_ROOT + 'jquery_ui/'
DYNAMICFORMS_VUE = DYNAMICFORMS_ROOT + 'vue/'


COMPONENT_DEF_RENDERER_FORMAT = 'componentdef'
COMPONENT_HTML_RENDERER_FORMAT = 'component'


class Settings(Struct):
    # Support for jQueryUI (this will be queried in dynamicforms.js)
    jquery_ui = False

    # if True, base_list template will render the HTML such that it will display dialog
    #   Make sure you {% include DYNAMICFORMS.modal_dialog_rest_template %} somewhere top-level in your html body
    # if False, the record will be displayed in a new page
    edit_in_dialog = True

    # Support for select2
    use_select2 = True

    # specifies the basepage template to be used for TemplateHTMLRenderer
    page_template = ''

    # specifies text to be displayed in grid when field's value is null
    null_text_table = 'null'

    preuploaded_file_margin_for_file_deletion_in_seconds: int = 86400  # 1 day

    allow_anonymous_user_to_preupload_files = False

    def __init__(self, data=None, **kwds):
        kwds.setdefault('page_template', DYNAMICFORMS_ROOT + 'page.html')
        super().__init__(data, **kwds)
        self.template = DYNAMICFORMS_BOOTSTRAP
        self.template_root = DYNAMICFORMS_ROOT
        self.login_url = s.LOGIN_URL

    def __to_dict__(self):
        res = {}
        res.update(super().__to_dict__())
        for p in dir(self):
            if not (p == 'clone' or p.startswith('_')):
                res[p] = getattr(self, p)
        return res

    # noinspection PyPep8Naming
    @property
    def DisplayMode(self):
        from .mixins import DisplayMode
        return {e.name: e.value for e in DisplayMode}  # A copy to be accessible in the templates

    def _get_components(self):
        return getattr(threading.current_thread(), 'is_component_renderer', False)

    def _set_components(self, value):
        threading.current_thread().is_component_renderer = value

    components = property(_get_components, _set_components)

    # ****************************************************************************
    # These are constants, generated from settings. They are shortcuts for quick use in templates and are specific
    # to the chosen template pack.
    # ****************************************************************************

    select2_form_field_class = property(lambda self: 'select2-field' if self.use_select2 else '')

    # Path to template for :samp:`<html><head>` tag JS & CSS includes, necessary for the chosen template pack.
    page_includes = property(lambda self: DYNAMICFORMS_ROOT + 'base_includes.html')

    # Path to base template for fields.
    field_base_template = property(lambda self: DYNAMICFORMS_ROOT + 'field/base_field.html')

    # Path to base template for forms.
    form_base_template = property(lambda self: DYNAMICFORMS_ROOT + 'base_form.html')

    # Path to base template for forms.
    table_base_template = property(lambda self: DYNAMICFORMS_ROOT + 'base_list.html')

    # Path to base template for forms.
    table_filter_base_template = property(lambda self: DYNAMICFORMS_ROOT + 'base_table_filter.html')

    # Path to base template for table body.
    table_body_base_template = property(lambda self: DYNAMICFORMS_ROOT + 'base_table_body.html')

    # Path to template for modal dialog
    modal_dialog_rest_template = property(lambda self: DYNAMICFORMS_ROOT + 'modal_dialog_rest.html')

    # classes to use on form buttons
    form_button_classes = property(lambda self: '')
    form_button_classes_cancel = property(lambda self: '')
    form_button_classes_primary = property(lambda self: '')
    form_button_classes_secondary = property(lambda self: '')

    select2_include = property(lambda self: DYNAMICFORMS_ROOT + 'base_includes_select2.html')

    progress_dialog_title = _('Performing operation...')


def if3_4(if3, if4):
    def inner(self):
        if self.bootstrap_version == 'v4':
            return if4
        return if3

    return inner


class SettingsBootstrap(Settings):
    # Supported Bootstrap versions are v3 and v4
    bootstrap_version = 'v4'

    def __init__(self, data=None, **kwds):
        super().__init__(data, **kwds)
        self.template = DYNAMICFORMS_BOOTSTRAP

    # select2 helper variables
    select2_theme = property(if3_4('bootstrap', 'bootstrap4'))
    select2_add_include = property(if3_4('select2/css/select2-bootstrap3.min.css',
                                         'select2/css/select2-bootstrap4.min.css'))

    # classes for card divs
    bs_card_class = property(if3_4('panel panel-default', 'card'))
    bs_card_header = property(if3_4('panel-heading df-card-header', 'card-header df-card-header'))
    bs_card_body = property(if3_4('panel-body df-card-body', 'card-body df-card-body'))

    # classes to use on form buttons
    form_button_classes = property(lambda self: 'btn ml-1')
    form_button_classes_cancel = property(lambda self: '')
    form_button_classes_primary = property(lambda self: 'btn-primary')
    form_button_classes_secondary = property(lambda self: 'btn-secondary')


class SettingsJqueryUI(Settings):
    jquery_ui = True

    def __init__(self, data=None, **kwds):
        super().__init__(data, **kwds)
        self.template = DYNAMICFORMS_JQUERY_UI

    # classes to use on form buttons
    form_button_classes = property(lambda self: 'ui-button ui-corner-all ui-widget')
    form_button_classes_cancel = property(lambda self: 'close-btn')
    form_button_classes_primary = property(lambda self: 'ui-state-highlight')
    form_button_classes_secondary = property(lambda self: '')


def get_settings():
    """
    Let's parse settings from settings.py

    :return: Settings class
    """
    df = Struct(
        template=DYNAMICFORMS_BOOTSTRAP,
    )
    df = df.clone(**getattr(s, 'DYNAMICFORMS', {}))
    template = df.template
    if template == DYNAMICFORMS_BOOTSTRAP:
        return SettingsBootstrap(**df.__to_dict__())
    return SettingsJqueryUI(**df.__to_dict__())


DYNAMICFORMS = get_settings()


def version_check(checked_version, min_version):
    """
    Checks whether checked version is higher or equal to given min version
    :param checked_version: version being checked
    :param min_version: minimum allowed version
    :return: True when checked version is high enough
    """

    if not checked_version or checked_version == 'None':
        return False
    return Version(checked_version, scheme=Pep440VersionScheme) >= Version(min_version, scheme=Pep440VersionScheme)
