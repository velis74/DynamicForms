---
sidebarDepth: 3
---

# Using Vue in Markdown

In VitePress, each markdown file is compiled into HTML and then processed as a Vue Single-File Component. This means you
can use any Vue features inside the markdown, including dynamic templating, using Vue components, or arbitrary in-page
Vue component logic by adding a `<script>` tag.

It is also important to know that VitePress leverages Vue 3's compiler to automatically detect and optimize the purely
static parts of the markdown. Static contents are optimized into single placeholder nodes and eliminated from the page's
JavaScript payload. They are also skipped during client-side hydration. In short, you only pay for the dynamic parts on
any given page.

## Templating

### Interpolation

Each Markdown file is first compiled into HTML and then passed on as a Vue component to the Vite process pipeline. This
means you can use Vue-style interpolation in text:

**Input**

```md
{{ 1 + 1 }}
```

**Output**

<div class="language-text"><pre><code>{{ 1 + 1 }}</code></pre></div>

### Directives

Directives also work:

**Input**

```md
<span v-for="i in 3">{{ i }} </span>
```

**Output**

<div class="language-text"><pre><code><span v-for="i in 3">{{ i }} </span></code></pre></div>

## Escaping

By default, fenced code blocks are automatically wrapped with `v-pre`. To display raw mustaches or Vue-specific syntax
inside inline code snippets or plain text, you need to wrap a paragraph with the `v-pre` custom container:

**Input**

```md
::: v-pre
`{{ This will be displayed as-is }}`
:::
```

**Output**

::: v-pre
`{{ This will be displayed as-is }}`
:::

## Using Components

When you need to have more flexibility, VitePress allows you to extend your authoring toolbox with your own Vue
Components.

### Importing components in markdown

If your components are going to be used in only a few places, the recommended way to use them is to importing the
components in the file where it is used.

```md
<script setup>
import CustomComponent from './CustomComponent.vue'
var data = [1,2,3,4,5];
</script>

# Docs

This is a .md using a custom component

<CustomComponent/>

Example Bellow:
```

[comment]: <> (<script setup>)

[comment]: <> (    import CustomComponent from './CustomComponent.vue';)

[comment]: <> (    var data = [1,2,3,4,5];)

[comment]: <> (</script>)

[comment]: <> (<CustomComponent :data="data"/>)

DF table

<div>
<div id="modal-app"></div>
<div id="df-app"></div>
</div>

<script setup>
    var params = {"uuid":"3d4bbd12-93c6-11ec-addb-1e00333c5875","titles":{"table":"Hidden fields list","new":"New hidden fields object","edit":"Editing hidden fields object"},"columns":[{"help_text":null,"uuid":"3d4b47b0-93c6-11ec-addb-1e00333c5875","name":"id","label":"ID","read_only":true,"table_classes":"","ordering":"ordering asc seg-1","alignment":"right","visibility":{"table":10,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false},{"help_text":null,"uuid":"3d4b2f32-93c6-11ec-addb-1e00333c5875","name":"df_control_data","label":"Df control data","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false},{"help_text":null,"uuid":"3d4b3428-93c6-11ec-addb-1e00333c5875","name":"df_prev_id","label":"Df prev id","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false},{"help_text":null,"uuid":"3d4b3b8a-93c6-11ec-addb-1e00333c5875","name":"row_css_style","label":"Row css style","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false},{"help_text":"Enter abc to hide unit field","uuid":"3d4b4f08-93c6-11ec-addb-1e00333c5875","name":"note","label":"Note","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":20,"min_length":null},"allow_null":false,"textarea":false},{"help_text":null,"uuid":"3d4b567e-93c6-11ec-addb-1e00333c5875","name":"unit","label":"Unit","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetSelect","input_type":"text","table":"df-tablecell-plaintext","multiple":false,"allow_tags":false,"field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false,"choices":[{"id":null,"text":"No additional data"},{"id":"pcs","text":"Pieces"},{"id":"wt","text":"Weight"},{"id":"cst","text":"Custom"}],"allow_tags":false},{"help_text":null,"uuid":"3d4b5ec6-93c6-11ec-addb-1e00333c5875","name":"int_fld","label":"Quantity","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"right","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false},{"help_text":"Feel free to use a decimal point / comma","uuid":"3d4b972e-93c6-11ec-addb-1e00333c5875","name":"qty_fld","label":"Weight","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"decimal","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"#DFTableCellFloat","table_show_zeroes":true,"step":"0.1","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false},{"help_text":"Enter additional info here","uuid":"3d4ba17e-93c6-11ec-addb-1e00333c5875","name":"cst_fld","label":"Comment","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":80,"min_length":null},"allow_null":true,"textarea":false},{"help_text":"Now that you have shown me, please enter something","uuid":"3d4ba908-93c6-11ec-addb-1e00333c5875","name":"additional_text","label":"Additional text","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":80,"min_length":null},"allow_null":true,"textarea":false},{"uuid":"","name":"#actions-row_end","label":"Actions","read_only":false,"alignment":"left","table_classes":"","ordering":"","render_params":{},"help_text":"","visibility":{"table":10},"allow_null":false}],"actions":{"add":{"position":"HEADER","field_name":null,"name":"add","action_js":"dynamicforms.newRow('{% url url_reverse|add:'-detail' pk='new' format='html' %}', 'record', __TABLEID__);","action":null,"label":"+ Add","title":"Add new record","icon":"add-circle-outline","classes":null},"edit":{"position":"ROW_CLICK","field_name":null,"name":"edit","action_js":"dynamicforms.editRow('{% url url_reverse|add:'-detail' pk='__ROWID__' format='html' %}'.replace('__ROWID__', $(event.target.parentElement).closest('tr[class=\"df-table-row\"]').attr('data-id')), 'record', __TABLEID__);","action":null,"label":"Edit","title":"Edit record","icon":"pencil-outline","classes":null},"delete":{"position":"ROW_END","field_name":null,"name":"delete","action_js":"dynamicforms.deleteRow('{% url url_reverse|add:'-detail' pk=row.id %}', {{row.id}}, 'record', __TABLEID__);","action":null,"label":"Delete","title":"Delete record","icon":"trash-outline","classes":null}},"record":null,"filter":null,"dialog":{"rows":[{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":null,"uuid":"3d4b47b0-93c6-11ec-addb-1e00333c5875","name":"id","label":"ID","read_only":true,"table_classes":"","ordering":"ordering asc seg-1","alignment":"right","visibility":{"table":10,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false}},{"type":"column","field":{"help_text":null,"uuid":"3d4b2f32-93c6-11ec-addb-1e00333c5875","name":"df_control_data","label":"Df control data","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false}},{"type":"column","field":{"help_text":null,"uuid":"3d4b3428-93c6-11ec-addb-1e00333c5875","name":"df_prev_id","label":"Df prev id","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false}},{"type":"column","field":{"help_text":null,"uuid":"3d4b3b8a-93c6-11ec-addb-1e00333c5875","name":"row_css_style","label":"Row css style","read_only":true,"table_classes":"","ordering":"","alignment":"left","visibility":{"table":5,"form":5},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":false,"textarea":false}},{"type":"column","field":{"help_text":"Enter abc to hide unit field","uuid":"3d4b4f08-93c6-11ec-addb-1e00333c5875","name":"note","label":"Note","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":20,"min_length":null},"allow_null":false,"textarea":false}}]},{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":null,"uuid":"3d4b567e-93c6-11ec-addb-1e00333c5875","name":"unit","label":"Unit","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetSelect","input_type":"text","table":"df-tablecell-plaintext","multiple":false,"allow_tags":false,"field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false,"choices":[{"id":null,"text":"No additional data"},{"id":"pcs","text":"Pieces"},{"id":"wt","text":"Weight"},{"id":"cst","text":"Custom"}],"allow_tags":false}}]},{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":null,"uuid":"3d4b5ec6-93c6-11ec-addb-1e00333c5875","name":"int_fld","label":"Quantity","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"right","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false}}]},{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":"Feel free to use a decimal point / comma","uuid":"3d4b972e-93c6-11ec-addb-1e00333c5875","name":"qty_fld","label":"Weight","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"decimal","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"number","table":"#DFTableCellFloat","table_show_zeroes":true,"step":"0.1","field_class":"form-control","label_after_element":false,"container_class":"form-group"},"allow_null":true,"textarea":false}}]},{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":"Enter additional info here","uuid":"3d4ba17e-93c6-11ec-addb-1e00333c5875","name":"cst_fld","label":"Comment","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":80,"min_length":null},"allow_null":true,"textarea":false}}]},{"component":"DFFormRow","columns":[{"type":"column","field":{"help_text":"Now that you have shown me, please enter something","uuid":"3d4ba908-93c6-11ec-addb-1e00333c5875","name":"additional_text","label":"Additional text","read_only":false,"table_classes":"","ordering":"ordering unsorted","alignment":"left","visibility":{"table":10,"form":10},"render_params":{"form":"DFWidgetInput","input_type":"text","table":"df-tablecell-plaintext","field_class":"form-control","label_after_element":false,"container_class":"form-group","max_length":80,"min_length":null},"allow_null":true,"textarea":false}}]}],"actions":{"form_init":{"name":"form_init","action_js":"examples.hide_fields_on_show(\"{{ serializer.uuid }}\");","action":null},"cancel":{"uuid":"3d4bb16e-93c6-11ec-addb-1e00333c5875","element_id":"cancel-3d4bbd12-93c6-11ec-addb-1e00333c5875","type":"CANCEL","positions":["dialog","form"],"name":"cancel","action_js":false,"action":null,"label":"Cancel","title":"Cancel","icon":null,"classes":"btn ml-1 btn-secondary "},"submit":{"uuid":"3d4bb33a-93c6-11ec-addb-1e00333c5875","element_id":"submit-3d4bbd12-93c6-11ec-addb-1e00333c5875","type":"SUBMIT","positions":["dialog","form"],"name":"submit","action_js":false,"action":null,"label":"Save changes","title":"Save changes","icon":null,"classes":"btn ml-1 btn-primary "}},"component_name":"ExampleHiddenLayout"},"detail_url":"http://localhost:8000/hidden-fields/--record_id--.json","ordering_parameter":"ordering","ordering_style":null,"rows":{"prev":null,"next":null,"results":[{"id":"1","df_control_data":{"row_css_style":"","actions":{"edit":{},"delete":{}}},"df_prev_id":"","row_css_style":"","note":"demo","unit":"Pieces","int_fld":"2","qty_fld":"None","cst_fld":"None","additional_text":"add"}]},"list_url":"http://localhost:8000/hidden-fields.json"};
    console.log(createApp);
    // import dftable from '../../../../vue/src/components/DFTable.vue';

    // <div id="app"></div>
    // <div id="modal-app"></div>
    console.log(params);
    createApp('df-app', '<dftable/>', params, 'modal-app');
</script>

