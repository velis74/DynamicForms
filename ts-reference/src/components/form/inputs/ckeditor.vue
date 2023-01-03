<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
  </vuetify-input>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import TranslationsMixin from '@/components/util/translations.mixin';

import InputBase from './base.mixin';
import VuetifyInput from './input-vuetify.vue';

export default defineComponent({
  name: 'DFWidgetCKEditor',
  components: { VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
});
</script>
