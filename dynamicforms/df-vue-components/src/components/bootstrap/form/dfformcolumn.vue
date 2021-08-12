<template>
  <div class="col" v-if="isGroup">
    <div class="card">
      <div class="card-header">
        {{ def.title }}
      </div>
      <div class="card-body">
        <component :is="def.field.render_params.form.replace(/-/g, '')"
                   :def="def.field" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText"/>
      </div>
      <div class="card-footer" v-if="def.footer">
        {{ def.footer }}
      </div>
    </div>
  </div>
  <component v-else-if="isHidden"
             :is="def.field.render_params.form.replace(/-/g, '')"
             :def="def.field" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText"/>
  <div :class="'col' + columnClasses" v-else>
    <component :is="def.field.render_params.form.replace(/-/g, '')" v-on:onValueConfirmed="onValueConfirmed"
               :def="def.field" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText"/>
  </div>
</template>

<style>
  label {
    margin-inline-end: .5em;
  }
</style>

<script>
import DisplayMode from '@/logic/displayMode';
import dfwidgetinput from '@/components/bootstrap/widget/dfwidgetinput.vue';
import dfwidgetpassword from '@/components/bootstrap/widget/dfwidgetpassword.vue';
import dfwidgetckeditor from '@/components/bootstrap/widget/dfwidgetckeditor.vue';
import dfwidgetselect from '@/components/bootstrap/widget/dfwidgetselect.vue';

export default {
  name: 'dfformcolumn',
  props: {
    def: {
      type: Object,
      required: true,
    },
    data: {
      type: Object,
      required: true,
    },
    errors: {
      type: Object,
      required: true,
    },
    showLabelOrHelpText: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    isGroup() { return this.def.type === 'group'; },
    isHidden() {
      return this.def.field.visibility.form === DisplayMode.HIDDEN;
    },
    columnClasses() { return this.def.width_classes ? ` ${this.def.width_classes}` : ''; },
  },
  methods: {
    onValueConfirmed() {
      this.$emit('onValueConfirmed');
    },
  },
  components: {
    dfwidgetinput,
    dfwidgetpassword,
    dfwidgetckeditor,
    dfwidgetselect,
  },
};
</script>

<style scoped>

</style>
