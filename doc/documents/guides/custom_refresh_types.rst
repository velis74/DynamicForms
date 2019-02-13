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
       controls = ActionControls([
           # refreshType: record, Action : Add
           Action(label=_('+ Add'), title=_('Add new record'), icon='', position='header',
                  action="dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}'"
                         ", 'record', __TABLEID__);"),
           # refreshType: redirect, Action : Edit
           Action(label=_('Edit'), title=_('Edit record'), icon='', position='rowclick',
                  action="dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html'"
                         " %}'.replace('__ROWID__', $(event.target.parentElement).attr('data-id'))"
                         ", 'redirect:{% url 'validated-list' format='html' %}', __TABLEID__);"),
           # refreshType: custom JavaScript function, Action : Delete
           Action(label=_('Delete'), title=_('Delete record'), icon='', position='rowend',
                  action="dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', "
                  + "{{row.id}}, 'testRefreshType', __TABLEID__);"),
       ])

To use 'table', 'no refresh' or 'page' refresh types simply change 'record' inside of the action keyword argument in the declared Action.

If you would like to use your custom JavaScript function as a refresh type ('testRefreshType' in above example), you should declare the relevant function inside of corresponding template.

.. code-block:: html

    <script type="application/javascript">
      var testRefreshType = function () {
        alert("Custom function refresh type.");
      }
    </script>
