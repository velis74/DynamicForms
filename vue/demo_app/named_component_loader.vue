<template>
  <component :is="componentFinalName" :v-bind="componentProps" @title-change="(title) => $emit('title-change', title)"/>
</template>

<script>
import ThemeMixin from '../components/util/theme_mixin';

export default {
  name: 'NamedComponentLoader',
  mixins: [ThemeMixin],
  props: {
    componentName: { type: String, required: true },
    componentNameAddTemplateName: { type: Boolean, default: false },
    componentProps: { type: Object, required: true },
  },
  emits: ['title-change'],
  computed: {
    componentFinalName() {
      return (this.componentNameAddTemplateName ? this.theme.name.capitalised : '') + this.componentName;
    },
  },
};
</script>
