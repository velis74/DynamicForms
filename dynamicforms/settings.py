from django.conf import settings as s
from .struct import Struct

DYNAMICFORMS_BOOTSTRAP = 'dynamicforms/bootstrap/'
DYNAMICFORMS_JQUERY_UI = 'dynamicforms/jquery_ui/'


class Settings(Struct):

    # Support for jQueryUI (this will be queried in dynamicforms.js)
    jquery_ui = False

    # if True, base_list template will render the HTML such that it will display dialog
    #   Make sure you {% include DYNAMICFORMS.modal_dialog_template %} somewhere top-level in your html body
    # if False, the record will be displayed in a new page
    edit_in_dialog = True

    # Support for select2
    use_select2 = True

    # specifies the basepage template to be used for TemplateHTMLRenderer
    page_template = ''

    def __init__(self, data=None, **kwds):
        kwds.setdefault('page_template', DYNAMICFORMS_BOOTSTRAP + 'page.html')
        super().__init__(data, **kwds)
        self.template = DYNAMICFORMS_BOOTSTRAP

    def __to_dict__(self):
        res = {}
        res.update(super().__to_dict__())
        for p in dir(self):
            if not (p == 'clone' or p.startswith('_')):
                res[p] = getattr(self, p)
        return res

    # ****************************************************************************
    # These are constants, generated from settings. They are shortcuts for quick use in templates and are specific
    # to the chosen template pack.
    # ****************************************************************************

    select2_form_field_class = property(lambda self: 'select2-field' if self.use_select2 else '')

    # Path to template for :samp:`<html><head>` tag JS & CSS includes, necessary for the chosen template pack.
    page_includes = property(lambda self: self.template + 'base_includes.html')

    # Path to base template for fields.
    field_base_template = property(lambda self: self.template + 'field/base_field.html')

    # Path to base template for forms.
    form_base_template = property(lambda self: self.template + 'base_form.html')

    # Path to base template for forms.
    table_base_template = property(lambda self: self.template + 'base_list.html')

    # Path to base template for forms.
    table_filter_base_template = property(lambda self: self.template + 'base_table_filter.html')

    # Path to base template for table body.
    table_body_base_template = property(lambda self: self.template + 'base_table_body.html')

    # Path to template for modal dialog
    modal_dialog_template = property(lambda self: self.template + 'modal_dialog.html')


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
    select2_include = property(lambda self: self.template + 'base_includes_select2.html')
    select2_bs_css = property(if3_4('select2/css/select2-bootstrap3.min.css', 'select2/css/select2-bootstrap4.min.css'))

    # classes for card divs
    bs_card_class = property(if3_4('panel panel-default', 'card'))
    bs_card_header = property(if3_4('panel-heading', 'card-header'))
    bs_card_body = property(if3_4('panel-body', 'card-body'))

    page_includes = property(lambda self: self.template + ('base_includes_%s.html' % self.bootstrap_version))
    field_base_template = property(lambda self: self.template + ('field/base_field_%s.html' % self.bootstrap_version))
    modal_dialog_template = property(lambda self: self.template + ('modal_dialog_%s.html' % self.bootstrap_version))


class SettingsJqueryUI(Settings):
    jquery_ui = True

    def __init__(self, data=None, **kwds):
        kwds.setdefault('page_template', DYNAMICFORMS_JQUERY_UI + 'page.html')
        super().__init__(data, **kwds)
        self.template = DYNAMICFORMS_JQUERY_UI


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
