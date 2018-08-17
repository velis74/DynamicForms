import uuid as uuid_module


class UUIDMixIn(object):
    def __init__(self, *args, uuid: uuid_module.UUID=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()
