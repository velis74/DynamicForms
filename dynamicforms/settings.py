from django.conf import settings as s
from .struct import Struct

MODULE_PREFIX = 'DYNAMICFORMS_'


# TEMPLATE specifies the template pack that dynamicforms will use for rendering HTML forms,
# e.g. 'bootstrap', 'jQuery UI', etc.
TEMPLATE = getattr(s, MODULE_PREFIX + 'TEMPLATE', 'dynamicforms/bootstrap/')

# TEMPLATE_VARIANT offers a chance to do some things in the template pack differently. It can be used for anything from
# choosing version of the underlying framework (bootstrap 3 vs 4) or rendering various subsections differently
# (e.g. horizontally aligned form labels vs vertically aligned ones)
TEMPLATE_VARIANT = Struct(getattr(s, MODULE_PREFIX + 'TEMPLATE_VARIANT', dict(BOOTSTRAP_VERSION='v4')))


# This is a calculated constant specifying the HTML header includes providing js and css for desired Bootstrap version
BSVER_INCLUDES = TEMPLATE + ('base_includes_%s.html' % TEMPLATE_VARIANT.BOOTSTRAP_VERSION)
BSVER_FIELD_TEMPLATE = TEMPLATE + ('field/base_field_%s.html' % TEMPLATE_VARIANT.BOOTSTRAP_VERSION)

# these entire settings will be passed to context of each form render
CONTEXT_VARS = {k: v for k, v in globals().items() if k == k.upper()}
