<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText">
    <input slot="input" :id="def.uuid" :type="def.render_params.input_type"
           v-on:keyup.enter="onValueConfirmed(true)"
           v-on:input="onValueConfirmed(false)"
           v-on:change="onValueConfirmed(false)"
           :class="def.render_params.class"
           :name="def.name"
           :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
           :placeholder="def.placeholder" v-model="
/* eslint-disable */
data[def.name]"
           :pattern="def.render_params.pattern"
           :min="def.render_params.min" :max="def.render_params.max" :step="def.render_params.step"
           :minlength="def.render_params.minlength" :maxlength="def.render_params.maxlength"
           :size="def.render_params.size">
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';

export default {
  name: 'dfwidgetinput',
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
  methods: {
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
  },
  components: {
    dfwidgetbase,
  },
};
</script>

<style scoped>

</style>
