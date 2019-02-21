Custom refresh types
====================

DynamicForms supports six different refresh types, which control what happens after CRUD actions:

1. record - Triggers ajax request and updates single record in table without page reload.
2. table - Triggers ajax request and updates the whole table without page reload.
3. no refresh - Doesn't do anything.
4. page - Triggers page reload.
5. redirect:url - Redirects to your custom url.
6. custom JavaScript function - Triggers your custom JavaScript function.

You can set refresh type on each type of Action, either add, edit or delete inside of control variable of your serializer, which inherits from DynamicForms ModelSerializer.

Following example shows how you can set each of the refresh types.

.. code-block:: python

    :caption: examples/rest/refresh_types.py
    :name: examples/rest/refresh_types.py

    from dynamicforms import serializers
    from ..models import RefreshType


    class RefreshTypesSerializer(serializers.ModelSerializer):
       form_titles = {
           'table': 'Refresh type list',
           'new': 'New refresh type object',
           'edit': 'Editing refresh type object',
       }
    actions = Actions(
        # Add actions
        # refresh record
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh record)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'record', __TABLEID__);"),
        # refresh table
        TableAction(TablePosition.HEADER, label=_('+ Add (refresh table)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'table', __TABLEID__);"),
        # no refresh
        TableAction(TablePosition.HEADER, label=_('+ Add (no refresh)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'no refresh', __TABLEID__);"),
        # page reload
        TableAction(TablePosition.HEADER, label=_('+ Add (page reload)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'page', __TABLEID__);"),
        # redirect
        TableAction(TablePosition.HEADER, label=_('+ Add (redirect)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        TableAction(TablePosition.HEADER, label=_('+ Add (custom function)'), title=_('Add new record'),
                    action_js="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                              ", 'testRefreshType', __TABLEID__);"),

        # Edit actions
        TableAction(TablePosition.ROW_CLICK, label=_('Edit'), title=_('Edit record'),
                    action_js="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                              " %}'.replace('__ROWID__', $(event.target.parentElement).attr('data-id'))"
                              ", 'record', __TABLEID__);"),

        # Delete actions
        # refresh record
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh record)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'record', __TABLEID__);"),
        # refresh table
        TableAction(TablePosition.ROW_END, label=_('Delete (refresh table)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'table', __TABLEID__);"),
        # no refresh
        TableAction(TablePosition.ROW_END, label=_('Delete (no refresh)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # The following action is duplicated unnecessarily just to later eliminate it in suppress_action
        TableAction(TablePosition.ROW_END, name='del 1', label=_('Delete (no refresh)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'no refresh', __TABLEID__);"),
        # page reload
        TableAction(TablePosition.ROW_END, label=_('Delete (page reload)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'page', __TABLEID__);"),
        # redirect
        TableAction(TablePosition.ROW_END, label=_('Delete (redirect)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
        # custom function
        TableAction(TablePosition.ROW_END, label=_('Delete (custom function)'), title=_('Delete record'),
                    action_js="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                              + "{{row.id}}, 'testRefreshType', __TABLEID__);"),
    )

To use 'table', 'no refresh' or 'page' refresh types simply change 'record' inside of the action keyword argument in the declared Action.

If you would like to use your custom JavaScript function as a refresh type ('testRefreshType' in above example), you should declare the relevant function inside of corresponding template.

.. code-block:: html

    <script type="application/javascript">
      var testRefreshType = function () {
        alert("Custom function refresh type.");
      }
    </script>
