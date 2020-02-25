from django.db import migrations

from examples.migrations import add_relation, add_filter, add_page_load


class DynamicformsMigration(migrations.Migration):
    def apply(self, project_state, schema_editor, collect_sql=False):
        applied = super().apply(project_state, schema_editor, collect_sql)
        if '0003_filter_name' in self.name:
            add_relation(None, None)
            add_page_load(None, None)
            add_filter(None, None)
        return applied
