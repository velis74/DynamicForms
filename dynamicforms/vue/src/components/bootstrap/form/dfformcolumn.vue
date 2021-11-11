<template>
  <div v-if="isGroup" :class="cssClasses">
    <div class="card">
      <div class="card-header">
        {{ def.title }}
      </div>
      <div class="card-body">
        <component
          :is="def.field.render_params.form"
          :def="def.field"
          :data="data"
          :errors="errors"
          :show-label-or-help-text="showLabelOrHelpText"
        />
      </div>
      <div v-if="def.footer" class="card-footer">
        {{ def.footer }}
      </div>
    </div>
  </div>
  <component
    :is="def.field.render_params.form"
    v-else-if="isHidden"
    :def="def.field"
    :data="data"
    :errors="errors"
    :show-label-or-help-text="showLabelOrHelpText"
  />
  <div v-else :class="cssClasses + columnClasses">
    <component
      :is="def.field.render_params.form"
      :def="def.field"
      :data="data"
      :errors="errors"
      :show-label-or-help-text="showLabelOrHelpText"
      @onValueConfirmed="onValueConfirmed"
    />
  </div>
</template>

<script>
import DisplayMode from '../../../logic/displayMode';
import DFWidgetCheckbox from '../widget/dfwidgetcheckbox.vue';
import DFWidgetCKEditor from '../widget/dfwidgetckeditor.vue';
import DFWidgetDatetime from '../widget/dfwidgetdatetime.vue';
import DFWidgetFile from '../widget/dfwidgetfile.vue';
import DFWidgetInput from '../widget/dfwidgetinput.vue';
import DFWidgetPassword from '../widget/dfwidgetpassword.vue';
import DFWidgetSelect from '../widget/dfwidgetselect.vue';

export default {
  name: 'DFFormColumn',
  components: {
    DFWidgetInput, DFWidgetPassword, DFWidgetCKEditor, DFWidgetSelect, DFWidgetCheckbox, DFWidgetFile, DFWidgetDatetime,
  },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
    cssClasses: { type: String, default: 'col' },
  },
  computed: {
    isGroup() {
      return this.def.type === 'group';
    },
    isHidden() {
      return this.def.field.visibility.form === DisplayMode.HIDDEN;
    },
    columnClasses() {
      const classes = this.def.width_classes;
      return classes ? ` ${classes}` : '';
    },
  },
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
  },
};
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
