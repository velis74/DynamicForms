from django.conf import settings as s
from .struct import Struct

MODULE_PREFIX = 'DYNAMICFORMS_'

# TEMPLATE specifies the template pack that dynamicforms will use for rendering HTML forms,
# e.g. 'bootstrap', 'jQuery UI', etc.
TEMPLATE = getattr(s, MODULE_PREFIX + 'TEMPLATE', 'dynamicforms/')


# TEMPLATE_OPTIONS offers a chance to do some things in the template pack differently. It can be used for anything from
# choosing version of the underlying framework (bootstrap 3 vs 4) or rendering various subsections differently
# (e.g. horizontally aligned form labels vs vertically aligned ones)
TEMPLATE_OPTIONS = dict(
    # Supported Bootstrap versions are v3 and v4
    BOOTSTRAP_VERSION='v4',
    # Support for select2
    USE_SELECT2=True,
    # if True, base_list template will render the HTML such that it will display dialog
    #   Make sure you {% include DF.MODAL_DIALOG %} somewhere top-level in your html body
    # if False, the record will be displayed in a new page
    EDIT_IN_DIALOG=True,
    # Support for jQueryUI
    JQUERY_UI=False
)

MODAL_DIALOG = 'modal_dialog'

# Ignore Bootstrap and Select2 if JQUERY_UI=True
if TEMPLATE_OPTIONS['JQUERY_UI']:
    TEMPLATE += 'jquery_ui/'

    TEMPLATE_OPTIONS['BOOTSTRAP_VERSION'] = None
    TEMPLATE_OPTIONS['USE_SELECT2'] = False
    TEMPLATE_OPTIONS.update(getattr(s, MODULE_PREFIX + 'TEMPLATE_OPTIONS', {}))
    TEMPLATE_OPTIONS = Struct(TEMPLATE_OPTIONS)

    # PAGE_TEMPLATE specifies the basepage template to be used for TemplateHTMLRenderer
    PAGE_TEMPLATE = getattr(s, MODULE_PREFIX + 'PAGE_TEMPLATE', TEMPLATE + 'page.html')

    BSVER_INCLUDES = TEMPLATE + ('base_includes.html')
    BSVER_FIELD_TEMPLATE = TEMPLATE + ('field/base_field.html')
    BSVER_MODAL = TEMPLATE + MODAL_DIALOG + '.html'
else:
    # These are calculated constants specifying the HTML header includes providing js and css for desired Bootstrap
    # version
    TEMPLATE += 'bootstrap/'
    TEMPLATE_OPTIONS.update(getattr(s, MODULE_PREFIX + 'TEMPLATE_OPTIONS', {}))
    TEMPLATE_OPTIONS = Struct(TEMPLATE_OPTIONS)

    # PAGE_TEMPLATE specifies the basepage template to be used for TemplateHTMLRenderer
    PAGE_TEMPLATE = getattr(s, MODULE_PREFIX + 'PAGE_TEMPLATE', TEMPLATE + 'page.html')

    BSVER_INCLUDES = TEMPLATE + ('base_includes_%s.html' % TEMPLATE_OPTIONS.BOOTSTRAP_VERSION)
    BSVER_FIELD_TEMPLATE = TEMPLATE + ('field/base_field_%s.html' % TEMPLATE_OPTIONS.BOOTSTRAP_VERSION)
    BSVER_MODAL = TEMPLATE + MODAL_DIALOG + ('_%s.html' % TEMPLATE_OPTIONS.BOOTSTRAP_VERSION)

    SELECT2 = TEMPLATE + 'base_includes_select2.html'

# these entire settings will be passed to context of each form render
CONTEXT_VARS = {k: v for k, v in globals().items() if k == k.upper()}


def is_jquery_ui():
    # noinspection PyUnresolvedReferences
    return TEMPLATE_OPTIONS.JQUERY_UI
