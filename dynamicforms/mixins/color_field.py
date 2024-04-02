class ColorFieldMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_params["form_component_name"] = "DColor"
