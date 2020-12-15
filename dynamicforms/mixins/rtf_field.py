class RTFFieldMixin(object):

    def to_representation(self, instance, row_data=None):
        if not self.parent.is_filter:
            self.style.update({'base_template': 'rtf_field.html'})
        return super().to_representation(instance, row_data)
