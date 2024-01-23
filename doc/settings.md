# DynamicForms Configuration

Like much of django-based libraries, DynamicForms is also configured from settings.py.

## Activate DynamicForms in DRF

In order to activate DynamicFroms, you need to add its renderers to DRF configuration, like so:

::: code-group

```python [settings.py]
REST_FRAMEWORK = {
   'DEFAULT_RENDERER_CLASSES': (
       'rest_framework.renderers.JSONRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',
        'dynamicforms.renderers.ComponentDefRenderer',
   )
}
```

:::

DRF will remain in control of JSON & Browseable API renderers while we activate DynamicForms for `.html` renders.

::: info
The DRF renderers are taken from default DRF configuration. If it should change, feel free to change the setting as well.
:::

## List of settings

### DYNAMICFORMS_TEMPLATE
Specifies the template pack that dynamicforms will use for rendering HTML forms, e.g. 'bootstrap', 'jQuery UI', etc.

### DYNAMICFORMS_PAGE_TEMPLATE
Specifies the main page template to be used for plain rendering when you navigate to a ViewSet router URL.

Defaults to DYNAMICFORMS_TEMPLATE + 'page.html' (but currently, there's nothing there - see dynamicforms examples on how to specify base page template)

### DYNAMICFORMS_TEMPLATE_OPTIONS

Offers a chance to do some things in the template pack differently. It can be used for anything from choosing version
of the underlying framework (bootstrap 3 vs 4) or rendering various subsections differently (e.g. horizontally
aligned form labels vs vertically aligned ones or editing record in modal dialog vs editing in new page).

Supported bootstrap versions are v3 and v4.

### DYNAMICFORMS_MODAL_DIALOG

Name of template for modal dialog. It will be appended any version modifiers, i.e. bootstrap version postfix if
bootstrap template pack.

