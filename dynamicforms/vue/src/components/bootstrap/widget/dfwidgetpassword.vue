<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <div slot="input" class="input-group">
      <input
        :id="def.uuid"
        v-model="value"
        :type="passwordFieldType"
        :class="def.render_params.field_class"
        :name="def.name"
        :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
        :placeholder="def.placeholder"
        :value="value"
        :pattern="def.render_params.pattern"
      >
      <span :id="'pwf-' + def.uuid" class="input-group-text" @click.stop="toggle_password">
        <IonIcon :name="isPassword ? 'eye-outline' : 'eye-off-outline'" class="pass-icon"/>
      </span>
    </div>
  </DFWidgetBase>
</template>

<script>
import IonIcon from '../ionicon.vue';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetPassword',
  components: { IonIcon, DFWidgetBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      passwordFieldType: 'password',
      isPassword: true,
    };
  },
  computed: {
    value: {
      get: function get() { return this.data[this.def.name]; },
      set: function set(newVal) {
        this.data[this.def.name] = newVal; // eslint-disable-line
      },
    },
  },
  methods: {
    toggle_password() {
      this.isPassword = !this.isPassword;
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
  },
};
</script>

<style scoped>
.pass-icon {
  margin: -.1em;
}
</style>
