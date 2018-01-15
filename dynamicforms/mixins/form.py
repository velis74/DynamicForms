class Form(object):
    """
    PK for accessing auditing / undo records in database. generate using uuid.UUIDn(),
    e.g. from uuid import uuid1 -> uuid1(). Or use your IDE plugin, such as UUID Generator for Intellij Idea
    """
    uuid = None
