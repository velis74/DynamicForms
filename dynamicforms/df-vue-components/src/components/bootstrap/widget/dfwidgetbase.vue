<template>
  <input v-if="isHidden" type="hidden" :name="def.name" :value="data[def.name]"/>
  <div v-else :id="'container-' + def.uuid" :class="def.render_params.container_class">
    <slot name="error"><small v-if="getErrorText" :id="def.name + '-err'"
                             class="form-text text-danger">{{ getErrorText }}</small></slot>
    <dfwidgetbaselabel v-if="labelAfterElement === false" v-bind:data="data" v-bind:def="def">
    </dfwidgetbaselabel>
    <slot name="input"></slot>
    <dfwidgetbaselabel v-if="labelAfterElement" v-bind:data="data" v-bind:def="def">
    </dfwidgetbaselabel>
    <slot name="help"><small v-if="def.help_text" :id="def.name + '-help'"
                             class="form-text text-muted">{{ def.help_text }}</small></slot>
  </div>
</template>

<script>
import DisplayMode from '@/logic/displayMode';
import dfwidgetbaselabel from '@/components/bootstrap/widget/dfwidgetbaselabel.vue';

export default {
  name: 'dfwidgetbase',
  props: ['def', 'data', 'errors'],
  computed: {
    isHidden() {
      console.log(this.def);
      return this.def.visibility.form === DisplayMode.HIDDEN;
    },
    labelAfterElement() {
      return this.def.render_params.label_after_element;
    },
    getErrorText() {
      try {
        if (this.errors && this.errors[this.def.name]) return this.errors[this.def.name];
        // eslint-disable-next-line no-empty
      } catch (e) {}
      return '';
    },
  },
  components: {
    dfwidgetbaselabel,
  },
};
</script>

<style scoped>

</style>
