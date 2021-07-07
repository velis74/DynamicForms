<template>
  <dfwidgetbase :def="def" :data="data">
    <input slot="input" :id="def.uuid" :type="def.render_params.input_type"
           :class="def.render_params.field_class"
           :name="def.field_name"
           :aria-describedby="def.help_text ? def.field_name + '-help' : null"
           :placeholder="def.placeholder" :value="data[def.field_name]"
           :pattern="def.render_params.pattern"
           :min="def.render_params.min" :max="def.render_params.max" :step="def.render_params.step"
           :minlength="def.render_params.minlength" :maxlength="def.render_params.maxlength"
           :size="def.render_params.size">
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';

export default {
  name: 'widgetinput',
  props: ['def', 'data'],
  components: {
    dfwidgetbase,
  },
};
</script>

<style scoped>

</style>
