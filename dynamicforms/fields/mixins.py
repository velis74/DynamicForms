from typing import List
import uuid as uuid_module


class UUIDMixIn(object):
    def __init__(self, *args, uuid: uuid_module.UUID=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()


class OnChangeMixin(object):
    def __init__(self, *args, actions: List['Action']=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = actions or []
