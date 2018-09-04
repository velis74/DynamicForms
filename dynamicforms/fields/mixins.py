from typing import List
import uuid as uuid_module


class UUIDMixIn(object):
    """
    Is used in fields and serializers, so every field and serializer gets its unique id.

    In form where serializer is used, id is serializers uuid. Table with list of records has id »list-serializer.uuid«,
    in dialog id is »dialog-{serializer.uuid}« and save button's id on dialog is »save-{serializer.uuid}«

    Similar for fields: All inputs in HTML get id from field.uuid. Div that contains all that belongs to the field has
    »container-{field.uuid}« for id, label has »label-{field.uuid}« and help text (if exists) has »help-{field.uuid}«
    for id.
    """

    def __init__(self, *args, uuid: uuid_module.UUID=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = uuid or uuid_module.uuid1()


class OnChangeMixin(object):
    def __init__(self, *args, actions: List['Action']=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = actions or []
