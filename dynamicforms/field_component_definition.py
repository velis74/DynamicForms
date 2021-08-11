class FieldComponentDefinition(dict):

    def __init__(self,
                 uuid: str,
                 name: str,
                 label: str,
                 alignment: str,
                 table_classes: str,
                 visibility: dict,
                 render_params: dict,
                 ordering: str,
                 help_text: str,
                 ) -> None:
        super().__init__()
        dict.__init__(self, uuid=uuid, name=name, label=label, table_classes=table_classes, visibility=visibility,
                      render_params=render_params, alignment=alignment, ordering=ordering, help_text=help_text)
