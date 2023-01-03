<template>
  <component :is="getThemedComponentName('Form')" v-bind="$props"/>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import Form from '../form/form.mixin';
import ThemeMixin from '../util/theme.mixin';

export default defineComponent({
  name: 'DfForm',
  mixins: [ThemeMixin],
  props: Form.props, // the same props as in forms
});
</script>
