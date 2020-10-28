class NullIntegerMixin(object):
    def to_internal_value(self, data):
        if data == '' and self.allow_null:
            self.validators = []
            return None
        return super().to_internal_value(data)
